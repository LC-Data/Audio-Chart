from __future__ import division
import wave
import os
import math
import audioop
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import vlc
import subprocess
import re
from collections import OrderedDict

plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
plt.rcParams['animation.convert_path'] = '/usr/bin/convert'


def inputData():

	graphData = [];

	with open('blizzSmall.txt', 'r') as f:
	    for line in f:
	       graphData.append(float(line.rstrip()));		### If this is not appended as a float, it will default to string which LUCKILY still sorted as numbers
	    #add error handling, and return something to pass perhaps
		#print ("number of data points in this sample... " + str(len(graphData))), '\n';
	return graphData;



def noteSet():			#This should eventually take an instrument/set of notes as a parameter

	notesDirectory = "./violinWavs2/";						#path to your music note .wav files
	notes = [];																#array of the above files
	notesWithPath = [];													#array of the above files including the path!
	
	for note in os.listdir(notesDirectory):
		notes.append(note);
	
	print ("The list of notes we are using is: "),notes, '\n';		#this syntax seems out of place
	notes.sort();
	print ("The ORDERED list of notes we are using is: "),notes, '\n';

	for i in range(0, len(notes)):
		notes[i] = str(notesDirectory + notes[i])

	return notes;



def writeAudio(data, newFirstNote, testSamp, newSecondNote, trigger, indexOne, indexTwo):

	indexOne = indexOne;
	indexTwo = indexTwo;
	
	if trigger == False:
		data[0][1] = newFirstNote + testSamp + newSecondNote;
		del data[1];
		cascadingOverlap(data, indexOne, indexTwo);

	else:
		data[0][1] = newFirstNote + testSamp + newSecondNote;
		del data[1];

		p = wave.open('./TESTAUDIO.wav', 'wb');			#writing audio data
		p.setparams(data[0][0]);

		for i in range(0, len(data)):
			p.writeframes(data[i][1])
		getRate = p.getparams();
		print ("PARAMETERS WRITTEN ARE - ", getRate)
		p.close()



def cascadingOverlap(data, indexOne, indexTwo):

	#print indexOne
	if len(data[indexTwo][1]) > len(data[indexOne][1]):
		theOverlapSize = math.trunc(len(data[indexOne][1]) * 0.50);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!
	else:
		theOverlapSize = math.trunc(len(data[indexTwo][1]) * 0.50);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!

	print ("The length of the first note in bytes is " + str(len(data[indexOne][1])));
	print ("The length of the second note in bytes is " + str(len(data[indexTwo][1])));
	print ("The length of the OVERLAP in bytes is " + str(theOverlapSize));

	newFirstNote = data[indexOne][1][: - theOverlapSize];		##	"cut" the first audio file to exclude the trailing lengh of the overlap
	newSecondNote = data[indexTwo][1][theOverlapSize:];		## same to the second (the audio is cut from the beginnning of this note)

	if len(newFirstNote) %2 != 0:
		print("The number of bytes in the first note is uneven!!=-=-=-=-=-=-=-=-=-", len(newFirstNote));
		newFirstNote = data[indexOne][1][: - (theOverlapSize) - 1];
		print("Attempted to correct byte length=-=-=-=-=-=-", len(newFirstNote));
#		newSecondNote = data[indexTwo][1][ - (theOverlapSize) - 1:];			#is this line just wrong?


	if (len(data[indexOne][1][:theOverlapSize]) % 2 == 0):
		overlapPart1 = data[indexOne][1][ - (theOverlapSize) : ];
		print "even number of frames."
		print (len(overlapPart1))

	else:
		print "ODD AS FUDGE"
		print (len(data[indexOne][1][:theOverlapSize]))
		overlapPart1 = data[indexOne][1][ - (theOverlapSize - 1) : ];
		print ("NOW EVEN AS FUDGE!", len(overlapPart1))


	if (len(data[indexTwo][1][:theOverlapSize]) % 2 == 0):
		overlapPart2 = data[indexTwo][1][ :  theOverlapSize ];
		print "even number of frames."
		print (len(overlapPart2))

	else:
		print "ODD AS FUDGE"
		print (len(data[indexTwo][1][:theOverlapSize]))
		overlapPart2 = data[indexTwo][1][ :  (theOverlapSize - 1)];
		print ("NOW EVEN AS FUDGE!", len(overlapPart2))


	#print ("The length of the first note without it's overlap is " + str(len(newFirstNote)));

	data[indexOne][1] = data[indexOne][1][:theOverlapSize]; 	#make wav segments to "add"(overlap) the same size -- this is required.

	print ("The length of the first overlap in bytes is " + str(len(overlapPart1)))

	print ("The length of the second overlap in bytes is " + str(len(overlapPart2)))

	testSamp = audioop.add(overlapPart1, overlapPart2, 2);	#This is an overlap


	if len(data) == 2:	#end condition, because indexOne is +1 on secondVar, but indexTwo takes the note AFTER indexOne
		
		writeAudio(data, newFirstNote, testSamp, newSecondNote, True, indexOne, indexTwo)
		drawAndSave();

	else:
		writeAudio(data, newFirstNote, testSamp, newSecondNote, False, indexOne, indexTwo)




def averagize(graphData, notes):

	data = [];
	numOfNotes = len(notes);
	numOfDataPoints = len(graphData);
	notesPerDataPoint = int(numOfDataPoints/numOfNotes) +1;				#+1 this just to make sure there are no rounding down errors (there might not be, anyway)
	finalNotes = [];	#the final notes in order

	print ("Number of notes is "), numOfNotes, "\n";
	print ("Number of data points is "), numOfDataPoints, "\n";
	print ("The number of 'data points per notes' is "), notesPerDataPoint, "\n";

	newListOfDataPoints = graphData[0::notesPerDataPoint];		### new list of data extracts every 'notesPerDataPoint'th index from graphData

	print ("The length of the new list of data points is: "), len(newListOfDataPoints);

	print ("The new list of data points (determined by the number of notes to data points - and picking at set intervals) is: "), newListOfDataPoints;

	print len(newListOfDataPoints), "\n";
	#print len()
	newListOfDataPoints = [int(float(x)) for x in newListOfDataPoints];

	sortedNewListOfDataPoints = newListOfDataPoints[:];
	sortedNewListOfDataPoints.sort();			## maybe refactor this in to one line with newListOfDataPoints declaration.
	#these are sorted so they can be linked to the notes from highest to lowest etc, maybe refactor this too, just sort the list...

	print notes, "\n\n\n\n\n";
	print newListOfDataPoints, "\n\n\n\n\n";
	
	notesTiedToData = OrderedDict(zip(sortedNewListOfDataPoints, notes));	#zips your notes and data together in order from lowest to highest or what have you

	minVal = (min(notesTiedToData, key=notesTiedToData.get));
	print("MIN VALUE IS, ", minVal);
	maxVal = (max(notesTiedToData, key=notesTiedToData.get));
	print("MAX VALUE IS, ", maxVal);

	notesTiedToData[maxVal] = './violinWavs2/z.wav';				# Turns the highest data value in to a clashing cymbal sound
	#notesTiedToData[minVal] = './violinWavs2/ZZZZZZZZZZZZZZZZZZZZCRASHHHHHHH.wav';		#lowest in to whatever sound.


	print notesTiedToData, "\n\n\n\n\n";

	print notesTiedToData.keys(), " THESE ARE THE KEYS \n\n";
	
	for i in range(0,len(newListOfDataPoints)):
		w = wave.open(notesTiedToData[newListOfDataPoints[i]], 'rb');
		data.append( [w.getparams(), w.readframes(w.getnframes())] );
		w.close();

	for x in newListOfDataPoints:
		finalNotes.append(notesTiedToData[x]);			#THIS JUST LET YOU SEE WHAT THE NOTES WILL LOOK LIKE, THIS ARRAY ISNT ACTUALLY USED, THE DATA JUST GETS WRITTEN

	print newListOfDataPoints;
	print ("THIS IS THE FINAL SET OF NOTES TO BE WRITTEN!!!\n\n\n\n", finalNotes);

	cascadingOverlap(data, 0, 1);	#overlap the notes, starting with note[0] and note [1]




def drawAndSave():

	def update_line(num, line):
	    i = X_VALS[num];
	    line.set_data( [i, i], [Y_MIN, Y_MAX]);
	    return line, ;


	fig = Figure();
	d = inputData();
	Y_MIN = min(d);
	Y_MAX = max(d);
	X_VALS = range(0,len(d));

	p = wave.open('./TESTAUDIO.wav', 'rb');			#reading audio data just for the params to calculate the length of the audio file
	frames = p.getnframes()
	rate = p.getframerate()

	secondsLong = frames/float(rate);

	print("seconds long is : ", float(secondsLong), type(secondsLong));
	print("Total number of audio frames is : ", float(frames));
	print("The audio framerate is : ", float(rate));
	print("SUCCESSS!!'/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\'");

	p.close();

	print("Length of data is: ", len(d));
	interval = floor(((secondsLong) * 1000)/len(X_VALS));	#need to play with this sometimes to sync the clash perfectly (adding +/-1 after secondsLong is experimental)

	fig = figure(figsize=(16.0, 9.0));
	ax = fig.add_subplot(1, 1, 1)
	ax.set_facecolor("k")
	print ("INTERVAL IS!!! - ", interval);
	plt.plot(d);
	l , v = plt.plot(0,0,5,0, linewidth=1, color= 'purple');
	plt.ylabel('$USD');		#change these -- they are the axes labels
	plt.xlabel('Time');

	line_anim = animation.FuncAnimation(fig, update_line, range(0,len(d)), fargs=(l, ), interval=(interval), blit=False, repeat=False);

	#plt.show();
	line_anim.save('TESTVIDEO.mp4');



averagize(inputData(), noteSet());

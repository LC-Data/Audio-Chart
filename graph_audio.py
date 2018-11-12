from __future__ import division
import wave
import os
import math
import audioop
from pylab import *
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
import vlc
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
plt.rcParams['animation.convert_path'] = '/usr/bin/convert'

import subprocess
import re
from collections import OrderedDict


def inputData():

	graphData = [];

	with open('BTCN.txt', 'r') as f:
	    for line in f:
	       graphData.append(float(line.rstrip()));		### If this is not appended as a float, it will default to string which LUCKILY still sorted as numbers
	    #add error handling, and return something to pass perhaps
		#print ("number of data points in this sample... " + str(len(graphData))), '\n';
	return graphData;



def noteSet():			#This should eventually take an instrument/set of notes as a parameter

	notesDirectory = "./violinWavs/";						#path to your music note .wav files
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

	firstVar = indexOne;			#just refactor this to use the parameter names instead of redeclaring them right here?
	secondVar = indexTwo;
	
	print firstVar
	if len(data[secondVar][1]) > len(data[firstVar][1]):
		theOverlapSize = math.trunc(len(data[firstVar][1]) * 0.50);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!
	else:
		theOverlapSize = math.trunc(len(data[secondVar][1]) * 0.50);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!

	print ("The length of the first note in bytes is " + str(len(data[firstVar][1])));
	print ("The length of the second note in bytes is " + str(len(data[secondVar][1])));
	print ("The length of the OVERLAP in bytes is " + str(theOverlapSize));

	newFirstNote = data[firstVar][1][: - theOverlapSize];		##	"cut" the first audio file to exclude the trailing lengh of the overlap
	newSecondNote = data[secondVar][1][theOverlapSize:];		## same to the second (the audio is cut from the beginnning of this note)

	if len(newFirstNote) %2 != 0:
		print("The number of bytes in the first note is uneven!!=-=-=-=-=-=-=-=-=-", len(newFirstNote));
		newFirstNote = data[firstVar][1][: - (theOverlapSize) - 1];
		print("Attempted to correct byte length=-=-=-=-=-=-", len(newFirstNote));
#		newSecondNote = data[secondVar][1][ - (theOverlapSize) - 1:];			#is this line just wrong?


	if (len(data[firstVar][1][:theOverlapSize]) % 2 == 0):
		overlapPart1 = data[firstVar][1][ - (theOverlapSize) : ];
		print "even number of frames."
		print (len(overlapPart1))

	else:
		print "ODD AS FUDGE"
		print (len(data[firstVar][1][:theOverlapSize]))
		overlapPart1 = data[firstVar][1][ - (theOverlapSize - 1) : ];
		print ("NOW EVEN AS FUDGE!", len(overlapPart1))


	if (len(data[secondVar][1][:theOverlapSize]) % 2 == 0):
		overlapPart2 = data[secondVar][1][ :  theOverlapSize ];
		print "even number of frames."
		print (len(overlapPart2))

	else:
		print "ODD AS FUDGE"
		print (len(data[secondVar][1][:theOverlapSize]))
		overlapPart2 = data[secondVar][1][ :  (theOverlapSize - 1)];
		print ("NOW EVEN AS FUDGE!", len(overlapPart2))

			## the end of the second note

	#print ("The length of the first note without it's overlap is " + str(len(newFirstNote)));

	data[firstVar][1] = data[firstVar][1][:theOverlapSize]; 	#make wav segments to "add"(overlap) the same size -- this is required.

	print ("The length of the first overlap in bytes is " + str(len(overlapPart1)))

	print ("The length of the second overlap in bytes is " + str(len(overlapPart2)))

	testSamp = audioop.add(overlapPart1, overlapPart2, 2);	#This is an overlap


	if len(data) == 2:	#end condition, because firstVar is +1 on secondVat, but secondVar takes the note AFTER firstVar
		
		writeAudio(data, newFirstNote, testSamp, newSecondNote, True, firstVar, secondVar)
		drawAndSave();

	else:
		writeAudio(data, newFirstNote, testSamp, newSecondNote, False, firstVar, secondVar)




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
	intNewListOfDataPoints = [int(float(x)) for x in newListOfDataPoints]

	cloneIntNewListOfDataPoints = intNewListOfDataPoints[:];			## maybe refactor this in to one line with newListOfDataPoints declaration.

	cloneIntNewListOfDataPoints.sort();			#these are sorted so they can be linked to the notes from highest to lowest etc, maybe refactor this too, just sort the list...

	print notes, "\n\n\n\n\n";
	print cloneIntNewListOfDataPoints, "\n\n\n\n\n";
	chronoList = intNewListOfDataPoints[:];	#this list is flipped so it is chronological oldest to newest -- will depend on your list of data

	notesTiedToData = OrderedDict(zip(cloneIntNewListOfDataPoints, notes));	#zips your notes and data together in order from lowest to highest or what have you

	minVal = (min(notesTiedToData, key=notesTiedToData.get));
	print("MIN VALUE IS, ", minVal);
	maxVal = (max(notesTiedToData, key=notesTiedToData.get));
	print("MAX VALUE IS, ", maxVal);

	notesTiedToData[maxVal] = './violinWavs/z.wav';				# Turns the highest data value in to a clashing cymbal sound
	#notesTiedToData[minVal] = './violinWavs/ZZZZZZZZZZZZZZZZZZZZCRASHHHHHHH.wav';		#lowest in to whatever sound.


	print notesTiedToData, "\n\n\n\n\n";

	print notesTiedToData.keys(), " THESE ARE THE KEYS \n\n";
	
	for i in range(0,len(chronoList)):
		w = wave.open(notesTiedToData[chronoList[i]], 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	for x in chronoList:
		finalNotes.append(notesTiedToData[x])			#THIS JUST LET YOU SEE WHAT THE NOTES WILL LOOK LIKE, THIS ARRAY ISNT ACTUALLY USED, THE DATA JUST GETS WRITTEN

	print chronoList
	print ("THIS IS THE FINAL SET OF NOTES TO BE WRITTEN!!!\n\n\n\n", finalNotes)

	cascadingOverlap(data, 0, 1);	#overlap the notes, starting with note[0] and note [1]




def drawAndSave():

	def update_line(num, line):
	    i = X_VALS[num];
	    line.set_data( [i, i], [Y_MIN, Y_MAX]);
	    return line, ;


	fig = Figure();
	d = inputData();
	#timeData222 = [];		### Maybe even just spoof this data, who cares. This is just needs to be (I think) the same length as the x values, just need data there.
	Y_MIN = min(d);
	Y_MAX = max(d);
	X_VALS = range(0,len(d));


	p = wave.open('./TESTAUDIO.wav', 'rb');			#reading audio data
	frames = p.getnframes()
	rate = p.getframerate()
	#getRate2 = p.getparams();		##probably dont need this, get's the parameters as a whole of this audio file.
	#print ("FINAL PARAMETERS ARE - ", getRate2);

	secondsLong = frames/float(rate);

	print("seconds long is : ", float(secondsLong), type(secondsLong));
	print("Total number of audio frames is : ", float(frames));
	print("The audio framerate is : ", float(rate));
	print("SUCCESSS!!'/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\'");

	p.close();

	"""
	with open('/home/nathan/hearCharts/BTCN.txt', 'r') as f:
	    for line in f:
	       timeData222.append(line.rstrip());
	    add error handling, and return something to pass perhaps
		print ("number of data points in this sample... " + str(len(graphData))), '\n';
	print timeData222;

	t = timeData222;
	"""

	print("Length of data is: ", len(d));
	interval = ceil((secondsLong * 1000)/len(X_VALS));

	"""
	process = subprocess.Popen(['ffmpeg',  '-i', './THEBOSSBATTLE2222sack.wav'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

	print matches['hours']
	print matches['minutes']
	print matches['seconds']
	"""

	fig = figure(figsize=(16.0, 9.0));

	#outputFPS = ceil(len(d)/secondsLong);

	#print("FPS IS -=0=-=-=0=-=-=0=-=-=0=- ", (len(d)/secondsLong), outputFPS);

	print ("INTERVAL IS!!! - ", interval);
	plt.plot(d);
	l , v = plt.plot(0,0,-5,0, linewidth=1, color= 'red');
	plt.ylabel('$USD');		#change these -- they are the axes labels
	plt.xlabel('Time');

	line_anim = animation.FuncAnimation(fig, update_line, range(0,len(d)), fargs=(l, ), interval=(interval), blit=True, repeat=False);

	#plt.show();
	line_anim.save('TESTVIDEO.mp4');

averagize(inputData(), noteSet());

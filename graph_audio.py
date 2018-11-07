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

import subprocess
import re




secondsLong = None;
placeholderList = [];

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
	global secondsLong;
	indexOne = indexOne;
	indexTwo = indexTwo;
	
	if trigger == False:
		data[0][1] = newFirstNote + testSamp + newSecondNote;
		del data[1]
		cascadingOverlap(data, indexOne, indexTwo);

	else:
		data[0][1] = newFirstNote + testSamp + newSecondNote;
		del data[1]

		p = wave.open('./THEBOSSBATTLE2222.wav', 'wb');
		p.setparams(data[0][0]);

		for i in range(0, len(data)):
			p.writeframes(data[i][1])
		getRate = p.getparams();
		print ("FRAME RATE IS - ", getRate)
		p.close()

		p = wave.open('./THEBOSSBATTLE2222.wav', 'rb');
		frames = p.getnframes()
		rate = p.getframerate()
		getRate2 = p.getparams();
		print ("FINAL FRAME RATE IS - ", getRate2);

		secondsLong = frames/float(rate);

		print("seconds long is : ", float(secondsLong), type(secondsLong));
		print("SUCCESSS!!'/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\'");

		p.close();


















def cascadingOverlap(data, indexOne, indexTwo):

	firstVar = indexOne;
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
		print("IT'S FUCKED!!=-=-=-=-=-=-=-=-=-", len(newFirstNote));
		newFirstNote = data[firstVar][1][: - (theOverlapSize) - 1];
		print("MAYBE IT'S UNFUCKED!=-=-=-=-=-=-", len(newFirstNote));
		newSecondNote = data[secondVar][1][ - (theOverlapSize) - 1:];



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

	print ("The length of the first note without it's overlap is " + str(len(newFirstNote)));

	data[firstVar][1] = data[firstVar][1][:theOverlapSize]; 	#make wav segments to "add"(overlap) the same size -- this is required.

	print ("The length of the first overlap in bytes is " + str(len(overlapPart1)))

	print ("The length of the second overlap in bytes is " + str(len(overlapPart2)))

	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	testSamp = audioop.add(overlapPart1, overlapPart2, 2);

	#firstVar = firstVar + 2;
	#secondVar = secondVar + 2;
	#print ("HELLO !!", firstVar)
	if len(data) == 2:	#end condition, because firstVar is +1 on secondVat, but secondVar takes the note AFTER firstVar
		
		writeAudio(data, newFirstNote, testSamp, newSecondNote, True, firstVar, secondVar)
	else:
		print(" IS NEW FIRST NOTE STIILLLLL FUDGED?!?!?!?!?!!?!? ----------------------------------------------------------", str(len(newFirstNote)))
		writeAudio(data, newFirstNote, testSamp, newSecondNote, False, firstVar, secondVar)





















def averagize(graphData, notes):
	global placeholderList
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

	cloneIntNewListOfDataPoints = intNewListOfDataPoints[:];

	cloneIntNewListOfDataPoints.sort();			#these are sorted so they can be linked to the notes from highest to lowest etc

	print notes, "\n\n\n\n\n";
	print cloneIntNewListOfDataPoints, "\n\n\n\n\n";
	chronoList = intNewListOfDataPoints[:];	#this list is flipped so it is chronological oldest to newest -- will depend on your list of data

	notesTiedToData = dict(zip(cloneIntNewListOfDataPoints, notes));	#zips your notes and data together in order from lowest to highest or what have you

	print notesTiedToData, "\n\n\n\n\n";

	print notesTiedToData.keys(), " THESE ARE THE KEYS \n\n";
	
	for i in range(0,len(chronoList)):
		w = wave.open(notesTiedToData[chronoList[i]], 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	for x in chronoList:
		finalNotes.append(notesTiedToData[x])			#THIS JUST LET YOU SEE WHAT THE NOTES WILL LOOK LIKE, THIS ARRAY ISNT ACTUALLY USED, THE DATA JUST GETS WRITTEN

	print chronoList
	placeholderList = chronoList;
	print finalNotes

	cascadingOverlap(data, 0, 1);










	

averagize(inputData(), noteSet());



########### TO DO ##########
# - KEEP REFACTORING ALL OF THIS CRAP -- 
# - RELATIVISTIC NOTES TO DATA... if the data spikes REALLY high the note should too!	(SOMEWHAT helped this issue with the octaves)
# - Choose chronological or reverse chronological data input.
# - In the test file I got .wav overlapping figured out with audioop library, write a method to chain overlap the notes and integrate it here
# 	- to do this the overlapped data needs to be the same length in bytes (or time in real life...), consider overlappinng a % of the incoming note's length to the end of
#	- the previous note by the same length.\\\\





fig = Figure();

#matplotlib.use("gtk")

#graphData222 = [];

timeData222 = [];


with open('/home/nathan/hearCharts/BTCN4.txt', 'r') as f:
    for line in f:
       timeData222.append(line.rstrip());
    #add error handling, and return something to pass perhaps
	#print ("number of data points in this sample... " + str(len(graphData))), '\n';
#print timeData222;

d = inputData();
t = timeData222;
Y_MIN = min(placeholderList);
Y_MAX = max(placeholderList);
X_VALS = range(0,len(d));



print ("SECONDS LONG ISSSSSSSSSSSSS-", secondsLong);
print("Length of data is: ", len(placeholderList));
interval = float((secondsLong * 1000)/len(X_VALS));

process = subprocess.Popen(['ffmpeg',  '-i', './THEBOSSBATTLE2222.wav'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout, stderr = process.communicate()
matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

print matches['hours']
print matches['minutes']
print matches['seconds']
print(len(d))

def update_line(num, line):
    i = X_VALS[num];
    line.set_data( [i, i], [Y_MIN, Y_MAX]);
    return line, ;


fig = figure(figsize=(6.0, 4.0));

print ("INTERVAL IS!!! - ", interval);
plt.plot(d);
l , v = plt.plot(0,0,0,0, linewidth=1, color= 'black');
plt.ylabel('$USD');
plt.xlabel('Time');

line_anim = animation.FuncAnimation(fig, update_line, range(0,len(d)), fargs=(l, ), interval=85, blit=True, repeat=False);
#zz = vlc.MediaPlayer("./THEBOSSBATTLE.wav");

#zz.play();

mywriter = animation.FFMpegWriter(fps=11.7233, bitrate=44100);			###########THE FPS NEEDS IS THE DETERMINING FACTOR IN THE LENGTH OF THE VIDEO SOMEHOW ??????
line_anim.save('mymovie44444.mp4',writer=mywriter)	#### To get the correct video length you need to divide (numOfDataPointsOnGraph)/(audio length in seconds) and use that as fps
plt.show();

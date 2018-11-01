from __future__ import division
import wave
import os


def inputData():

	graphData = [];

	with open('AAPL.txt', 'r') as f:
	    for line in f:
	       graphData.append(line.rstrip());
	    #add error handling, and return something to pass perhaps

		#print ("number of data points in this sample... " + str(len(graphData))), '\n';

	return graphData;



def noteSet():			#This should eventually take an instrument/set of notes as a parameter

	notesDirectory = "./violinWavs/";						#path to your music note .wav files
	notes = [];																#array of the above files
	notesWithPath = [];													#array of the above files including the path!
	#outfile = "soundsFINALBTCN.wav";								#name that you are going to use for your output file -- this should probably not be here
 	#data = [];	#the data that is extracted/read from your inputted .wave files -- ALSO SHOULD PROBABLY REALLLLY NOT BE HERE
 	#x = 0;
	
	for note in os.listdir(notesDirectory):
		notes.append(note);
	#	print("NOTE ADDED", x);
	#	x += 1;

	print ("The list of notes we are using is: "),notes, '\n';		#this syntax seems out of place
	notes.sort();
	print ("The ORDERED list of notes we are using is: "),notes, '\n';


	for i in range(0, len(notes)):
		notes[i] = str(notesDirectory + notes[i])

	return notes;


def averagize(graphData, notes):

	data = [];
	numOfNotes = len(notes);
	numOfDataPoints = len(graphData);
	notesPerDataPoint = int(numOfDataPoints/numOfNotes) +1;				#+1 this just to make sure there are no rounding down errors (there might not be, anyway)
	finalNotes = [];	#the final notes in order

	print ("Number of notes is "), numOfNotes, "\n";
	print ("Number of data points is "), numOfDataPoints, "\n";
	print ("The number of 'data points per notes' is "), notesPerDataPoint, "\n";

	newListOfDataPoints = graphData[0::notesPerDataPoint];
	print ("The new list of data points (determined by the number of notes to data points - and picking at set intervals) is: "), newListOfDataPoints;

	print len(newListOfDataPoints), "\n";
	#print len()
	intNewListOfDataPoints = [int(float(x)) for x in newListOfDataPoints]

	cloneIntNewListOfDataPoints = intNewListOfDataPoints[:];

	cloneIntNewListOfDataPoints.sort();			#these are sorted so they can be linked to the notes from highest to lowest etc

	print notes, "\n\n\n\n\n";
	print cloneIntNewListOfDataPoints, "\n\n\n\n\n";
	chronoList = intNewListOfDataPoints[::-1];	#this list is flipped so it is chronological oldest to newest -- will depend on your list of data

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
	print finalNotes

	outfile = "trashDump.wav"
	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])

	for i in range(1,len(data)):
		output.writeframes(data[i][1])
	output.close()


averagize(inputData(), noteSet());




########### TO DO ##########
# - KEEP REFACTORING ALL OF THIS CRAP -- 
# - RELATIVISTIC NOTES TO DATA... if the data spikes REALLY high the note should too!	(SOMEWHAT helped this issue with the octaves)
# - Choose chronological or reverse chronological data input.
# - In the test file I got .wav overlapping figured out with audioop library, write a method to chain overlap the notes and integrate it here
# 	- to do this the overlapped data needs to be the same length in bytes (or time in real life...), consider overlappinng a % of the incoming note's length to the end of
#	- the previous note by the same length.

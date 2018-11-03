from __future__ import division
import wave
import os
import math
import audioop



def inputData():

	graphData = [];

	with open('BTCN.txt', 'r') as f:
	    for line in f:
	       graphData.append(line.rstrip());
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



endAudio = [];

def writeAudio(newFirstNote, testSamp, newSecondNote, trigger):



	if trigger == False:
		endAudio.append(newFirstNote)
		endAudio.append(testSamp)
		endAudio.append(newSecondNote)


	else:
		endAudio.append(newFirstNote)
		endAudio.append(testSamp)
		endAudio.append(newSecondNote)


		p = wave.open('./THEBOSSBATTLE', 'wb');
		p.setparams((2, 2, 22050, 98993, 'NONE', 'not compressed'));

		for i in range(0, len(endAudio)):
			p.writeframes(endAudio[i])
		p.close()

		print("SUCCESSS!!")






def cascadingOverlap(data, indexOne, indexTwo):

	if len(data[indexTwo][1]) > len(data[indexOne][1]):
		theOverlapSize = math.trunc(len(data[indexOne][1]) * 0.3);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!
	else:
		theOverlapSize = math.trunc(len(data[indexTwo][1]) * 0.3);	 	## 	!!! THE OVERLAP (for now) HAS TO BE 0.5 OF THE SMALLER NOTE!!

	if (theOverlapSize) % 2 == 0:
		print ("Overlap is happily equal.");
	else:
		theOverlapSize = theOverlapSize - 1;


	print ("The length of the first note in bytes is " + str(len(data[indexOne][1])));
	print ("The length of the second note in bytes is " + str(len(data[indexTwo][1])));
	print ("The length of the OVERLAP in bytes is " + str(theOverlapSize));


	newFirstNote = data[indexOne][1][: - theOverlapSize];		##	"cut" the first audio file to exclude the trailing lengh of the overlap
	newSecondNote = data[indexTwo][1][theOverlapSize:];		## same to the second (the audio is cut from the beginnning of this note)


	if (len(data[indexOne][1][:theOverlapSize]) % 2 == 0):
		overlapPart1 = data[indexOne][1][ - (theOverlapSize) : ];
		#print "even number of frames."
		#print (len(overlapPart1))

	else:
		#print "ODD AS FUDGE"
		#print (len(data[indexOne][1][:theOverlapSize]))
		overlapPart1 = data[indexOne][1][ - (theOverlapSize - 1) : ];
		#print ("NOW EVEN AS FUDGE!", len(overlapPart1))




	if (len(data[indexTwo][1][:theOverlapSize]) % 2 == 0):
		overlapPart2 = data[indexTwo][1][ :  theOverlapSize ];
		#print "even number of frames."
		#print (len(overlapPart2))

	else:
		#print "ODD AS FUDGE"
		#print (len(data[indexTwo][1][:theOverlapSize]))
		overlapPart2 = data[indexTwo][1][ :  (theOverlapSize - 1)];
		#print ("NOW EVEN AS FUDGE!", len(overlapPart2))


	#print ("The length of the first note without it's overlap is " + str(len(newFirstNote)));

	data[indexOne][1] = data[indexOne][1][:theOverlapSize]; 	#make wav segments to "add"(overlap) the same size -- this is required.

	#print ("The length of the first overlap in bytes is " + str(len(overlapPart1)))

	#print ("The length of the second overlap in bytes is " + str(len(overlapPart2)))


	testSamp = audioop.add(overlapPart1, overlapPart2, 2);

	indexOne = indexOne + 2;
	indexTwo = indexTwo + 2;
	#indexOne = indexOne + 1;
	#indexTwo = indexTwo + 1;
	print ("HELLO !!", indexOne)

	print(indexOne, indexTwo)
	if indexOne == len(data) -1:	#end condition, because indexOne is +1 on secondVat, but indexTwo takes the note AFTER indexOne
		
		writeAudio(newFirstNote, testSamp, newSecondNote, True)
		
	else:
		writeAudio(newFirstNote, testSamp, newSecondNote, False)
		cascadingOverlap(data, indexOne, indexTwo)


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

	#print len(newListOfDataPoints), "\n";
	#print len()
	intNewListOfDataPoints = [int(float(x)) for x in newListOfDataPoints]

	cloneIntNewListOfDataPoints = intNewListOfDataPoints[:];

	cloneIntNewListOfDataPoints.sort();			#these are sorted so they can be linked to the notes from highest to lowest etc

	#print notes, "\n\n\n\n\n";
	#print cloneIntNewListOfDataPoints, "\n\n\n\n\n";
	chronoList = intNewListOfDataPoints;	#this list is flipped so it is chronological oldest to newest -- will depend on your list of data
				#this list is flipped so it is chronological oldest to newest -- will depend on your list of data




	notesTiedToData = dict(zip(cloneIntNewListOfDataPoints, notes));	#zips your notes and data together in order from lowest to highest or what have you

	#print notesTiedToData, "\n\n\n\n\n";

	#print notesTiedToData.keys(), " THESE ARE THE KEYS \n\n";
	
	for i in range(0,len(chronoList)):
		w = wave.open(notesTiedToData[chronoList[i]], 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()

	print ("data[0][0] IS THIS =================================>", data[0][0])

	for x in chronoList:
		finalNotes.append(notesTiedToData[x])			#THIS JUST LET YOU SEE WHAT THE NOTES WILL LOOK LIKE, THIS ARRAY ISNT ACTUALLY USED, THE DATA JUST GETS WRITTEN

	print chronoList
	print finalNotes

	cascadingOverlap(data, 0, 1);

averagize(inputData(), noteSet());



########### TO DO ##########
# - KEEP REFACTORING ALL OF THIS CRAP -- 
# - RELATIVISTIC NOTES TO DATA... if the data spikes REALLY high the note should too!	(SOMEWHAT helped this issue with the octaves)
# - Choose chronological or reverse chronological data input.
# - Overlapping DONE
# - keep refactoring, collect like pieces of data, simplify functions
# - IF A FILE/LIST IS PASSED WITH AN EVEN NUMBER OF VALUES IT WILL CRASH BECAUSE OF LINE 130/131 -- PUSHES THE INDEX OUT OF BOUNDS 

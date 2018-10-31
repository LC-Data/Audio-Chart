from __future__ import division
import wave
import os


graphData = [];

with open('BTCN.txt', 'r') as f:
    for line in f:
       graphData.append(line.rstrip());

print ("number of data points in this sample... " + str(len(graphData))), '\n';

notesDirectory = "/home/nathan/hearCharts/violinWavs/";	#path to your music note .wav files

notes = [];	#array of the above files
notesWithPath = [];	#array of the above files including the path!
outfile = "soundsFINALBTCN.wav";	#name that you are going to use for your output file
data = [];	#the data that is extracted/read from your inputted .wave files

for note in os.listdir(notesDirectory):
	notes.append(note);

print ("The list of notes we are using is: "),notes, '\n';

notes.sort();	#probably not needed because they are numerically ordered


print ("The ORDERED list of notes we are using is: "),notes, '\n';	#turns out it is needed??


for note in notes:
	notesWithPath.append(str(notesDirectory) + str(note));

#output = wave.open(outfile, 'wb')	#open an output file for the final wav
#output.setparams(data[0][0])	#find out what this shit does

#for i in range(0,len(data)):	#write all of the data/notes we have read
#	output.writeframes(data[i][1]);

	#output.writeframes(data[0][1])
	#output.writeframes(data[1][1])
	#output.writeframes(data[2][1])
#output.close();

print len(data)
def averagize(dataPoints, notes):
	numOfNotes = len(notes);
	numOfDataPoints = len(dataPoints);

	notesPerDataPoint = int(numOfDataPoints/numOfNotes) +1;

	print ("Number of notes is, %s", numOfNotes);
	print ("Number of data points is, %s", numOfDataPoints);
	print ("The number of 'notes per data points' is..., %s", notesPerDataPoint);

	newListOfDataPoints = dataPoints[0::notesPerDataPoint];
	print ("The new list of data points (determined by the number of notes to data points - and picking at set intervals) is: "), newListOfDataPoints;

	print len(newListOfDataPoints), "\n";
	#print len()
	intNewListOfDataPoints = [int(float(x)) for x in newListOfDataPoints]

	cloneIntNewListOfDataPoints = intNewListOfDataPoints[:];

	cloneIntNewListOfDataPoints.sort();			#these are sorted so they can be linked to the notes from highest to lowest etc

	print notes, "\n\n\n\n\n";
	print cloneIntNewListOfDataPoints, "\n\n\n\n\n";
	chronoList = intNewListOfDataPoints;	#this list is flipped so it is chronological oldest to newest -- will depend on your list of data

	notesTiedToData = dict(zip(cloneIntNewListOfDataPoints, notesWithPath));	#zips your notes and data together in order from lowest to highest or what have you

	print notesTiedToData, "\n\n\n\n\n";

	print notesTiedToData.keys(), " THESE ARE THE KEYS \n\n";
	finalNotes = [];	#the final notes in order

	for i in range(0,len(chronoList)):
		w = wave.open(notesTiedToData[chronoList[i]], 'rb')
		data.append( [w.getparams(), w.readframes(w.getnframes())] )
		w.close()



	for x in chronoList:
		finalNotes.append(notesTiedToData[x])			#THIS JUST LET YOU SEE WHAT THE NOTES WILL LOOK LIKE, THIS ARRAY ISNT ACTUALLY USED, THE DATA JUST GETS WRITTEN





	print chronoList
	print finalNotes



	output = wave.open(outfile, 'wb')
	output.setparams(data[0][0])

	for i in range(1,len(data)):
		output.writeframes(data[i][1])
	output.close()


averagize(graphData, notes)




########### TO DO ##########
# - REFACTOR ALL OF THIS CRAP
# - RELATIVISTIC NOTES TO DATA... if the data spikes REALLY high the note should too!
# - Choose chronological or reverse chronological data input.
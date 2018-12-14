import numpy as np
import wave
import struct
import matplotlib.pyplot as plt
 
# frequency is the number of times a wave repeats a second  --- Messing with the frequency gives us the different sound pitches(probably wrong terminology).
frequency = 250 
num_samples = 44100
 
# The sampling rate of the analog to digital convert
sampling_rate = 44100.0
amplitude = 32000 # corresponds to volume?
 
file = "./smallFreqs/GRAND"	#File name is split up in to 3 pieces like this in case we want to create multiple files, so we can increment the number
fileNum = 1
ext = ".wav"

	#this is an empty list, that will be populated with y-values from the resultant sine wave (I think)

for x in range(0,200):
	audioData = [];			
	sine_wave = [np.sin(2 * np.pi * frequency * x/sampling_rate) for x in range(num_samples)]	#generate the sin wave, which is a list of y-values (again, I think)
	frequency = frequency + 3;		#increment the frequency to change the sound on the next iteration
	for s in sine_wave:		#for each data value in the sine wave
		audioData.append(s);	#append that to our list


	nframes=num_samples		#These 5 vars are parameters for reading/writing .wav file
	comptype="NONE"
	compname="not compressed"
	nchannels=1
	sampwidth=2

	wav_file=wave.open((file + str(fileNum) + ext), 'w')		#open the wave file
	 
	wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))		#set the parameters

	for y in audioData:		#for each data point the the audioData list
		wav_file.writeframes(struct.pack('h', int(y*amplitude)))	#write the frames to the file

	fileNum = fileNum + 1;

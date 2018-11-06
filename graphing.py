from pylab import *
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure

fig = Figure();

#matplotlib.use("gtk")

graphData = [];

timeData = [];


with open('/home/nathan/hearCharts/BTCN.txt', 'r') as f:
    for line in f:
       graphData.append(float(line.rstrip()));
    #add error handling, and return something to pass perhaps
	#print ("number of data points in this sample... " + str(len(graphData))), '\n';
print graphData;

#graphData2 = np.array(graphData);

with open('/home/nathan/hearCharts/BTCN2.txt', 'r') as f:
    for line in f:
       timeData.append(line.rstrip());
    #add error handling, and return something to pass perhaps
	#print ("number of data points in this sample... " + str(len(graphData))), '\n';
print timeData;

d = graphData
t = timeData
Y_MIN = min(d)
Y_MAX = max(d)
X_VALS = range(0,len(graphData));


def update_line(num, line):
    i = X_VALS[num]
    line.set_data( [i, i], [Y_MIN, Y_MAX])
    return line, 


fig = figure(figsize=(6.0, 3.0))

plt.plot(d)
l , v = plt.plot(-6, -1, 6, 1, linewidth=2, color= 'red')
plt.ylabel('Sunlight')
plt.xlabel('Time')

line_anim = animation.FuncAnimation(fig, update_line, len(X_VALS), fargs=(l, ), interval=81, blit=True, repeat=True)

plt.show()

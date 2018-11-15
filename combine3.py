
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

cmd = 'ffmpeg -i TESTVIDEO.mp4 -i TESTAUDIO.wav  -c:v copy -c:a aac -strict experimental NUTSeezyblizzSmall.mp4'
subprocess.call(cmd, shell=True)                                     # "Muxing Done
print('Muxing Done')


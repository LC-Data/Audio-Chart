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

cmd = 'ffmpeg -y -i THEBOSSBATTLE2222sack.wav  -r 30 -i mymovie44444.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy SACCCCCKKKK.mkv'
subprocess.call(cmd, shell=True)                                     # "Muxing Done
print('Muxing Done')
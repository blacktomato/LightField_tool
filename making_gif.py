#!/usr/bin/env python
# coding=utf-8
##############################################################
 # File Name : making_gif.py
 # Purpose : Make a GIF
 # Creation Date : Sat 19 Aug 2017 08:43:02 PM CST
 # Last Modified : Sun 20 Aug 2017 01:12:59 AM CST
 # Created By : SL Chung
##############################################################
#Usage: 
#    python3 making_gif.py ./Img_Directory [./GIF_name]
import cv2
import numpy as np
import math
import sys
import os
from matplotlib import pyplot as plt
from matplotlib import animation
from python_tools import file_io

def build_gif(imgs, show_gif=True, save_gif=True, name=''):
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')

    ims = []
    for i in range(len(imgs)):
        im = plt.imshow(cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB))
        ims.append([im])

    im_ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=0, blit=False)
 
    if save_gif:
        im_ani.save(name + '.gif', writer='imagemagick')
 
    if show_gif:
        plt.show()
 
    return

if len(sys.argv) < 2:
    print('Error: need input directory of source of GIF!')
    sys.exit()

img_directory = sys.argv[1]
img_name = sorted([f for f in os.listdir(img_directory) if f.startswith("shift_") and f.endswith(".jpg")])

temp = img_name[:len(img_name)//2]
temp.reverse()
img_name[:len(img_name)//2] = temp

#for play back
double = img_name[1:-1]
double.reverse()
img_name.extend(double)

imgs = []

for idx, name in enumerate(img_name):
    fpath = os.path.join(img_directory, name)
    try:
        imgs.append( file_io.read_img(fpath) )
    except IOError:
        print("Could not read input file: %s" % fpath)
        sys.exit()

if len(sys.argv) == 3:
    print('Save the file as \'' + sys.argv[2] + '.gif\'')
    build_gif(imgs, True, True, sys.argv[2] )
else:
    print('Only show the GIF file...')
    build_gif(imgs, True, False)

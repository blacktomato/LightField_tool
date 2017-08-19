#!/usr/bin/env python
# coding=utf-8
##############################################################
 # File Name : LF_refocusing.py
 # Purpose : Refocus the Light Field Image
 # Creation Date : Wed 16 Aug 2017 02:04:54 PM CST
 # Last Modified : Sun 20 Aug 2017 01:15:39 AM CST
 # Created By : SL Chung
##############################################################
#Usage: 
#    python3 LF_refocusing.py ./Img_Directory
import cv2
import numpy as np
import math
import sys
import os
from matplotlib import pyplot as plt

from python_tools import file_io

#def imshow(window_name, img, start_x, start_y):
#    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#    cv2.resizeWindow(window_name, 400, 400)
#    cv2.moveWindow(window_name, start_x, start_y)
#    cv2.imshow(window_name, center_img)

def gen_shifted_img(params, light_field, delta_x, delta_y):
    shifted_img = np.zeros((params['height'], params['width'], 3))
    center_coordinate = (params['num_cams_x']//2 + 1, params['num_cams_y']//2 + 1)

    for i in range(params['num_cams_x']):
        for j in range(params['num_cams_y']):
            start_x = (center_coordinate[0] - i) * delta_x 
            start_y = (center_coordinate[1] - j) * delta_y
            temp = np.concatenate((light_field[i, j, start_x:, :, :], light_field[i, j, 0:start_x, :, :]), 0)
            temp = np.concatenate((temp[:, start_y:, :], temp[:, 0:start_y, :]), 1)
            shifted_img = shifted_img + temp

    shifted_img = shifted_img / ( params['num_cams_x'] * params['num_cams_y'])
    shifted_img = shifted_img.astype('uint8')
    return shifted_img

if len(sys.argv) < 2:
    print('Error: need input directory of source of GIF!')
    sys.exit()

LF_directory = sys.argv[1]

params = file_io.read_parameters(sys.argv[1])
light_field = file_io.read_lightfield(sys.argv[1])

center_img = light_field[ math.ceil(params['num_cams_x'] / 2), 
                          math.ceil(params['num_cams_y'] / 2), :, :, : ]
center_img = center_img.astype('uint8')

average_img = np.sum(light_field, (0, 1)) / ( params['num_cams_x'] * params['num_cams_y'])
average_img = average_img.astype('uint8')

shifted_img = gen_shifted_img(params, light_field, 1, 1);

window=[]
window.append('Original Center Img')
window.append('Average Img')
window.append('Shifted Img')

#start_x = 0
#start_y = 0
#imshow(window[0], center_img, start_x, start_y)
#
#start_x = start_x + 400;
#imshow(window[1], average_img, start_x, start_y)
#
#cv2.waitKey(0)
#cv2.destroyAllWindows()

plt.subplot(1,3,1),plt.imshow(cv2.cvtColor( center_img, cv2.COLOR_BGR2RGB))
plt.title(window[0]), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2),plt.imshow(cv2.cvtColor(average_img, cv2.COLOR_BGR2RGB))
plt.title(window[1]), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3),plt.imshow(cv2.cvtColor(shifted_img, cv2.COLOR_BGR2RGB))
plt.title(window[2]), plt.xticks([]), plt.yticks([])

plt.show()

if not os.path.exists('./shifted/'):
    os.makedirs('./shifted')

for i in range(11):
    i = i - 5
    s = gen_shifted_img(params, light_field, i, i);
    cv2.imwrite('./shifted/shift_' + str(i) + '.jpg', s)



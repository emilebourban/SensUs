# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 17:34:30 2019

@author: Emile
"""
import os
import scipy
import imageio
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.draw import circle_perimeter, circle
from utilities import smooth_background

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
#cxs, cys, radii = [240*5, 555*5, 1185, -260, 1295, 4235, 4220, 4300], [1555, 1480,20, 1570, 3045, 1472, -75, 3010], [330,330, 330, 330, 330, 330, 330, 330]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
#cxs, cys, radii = [1270, 2790, 1350, 1180], [1540, 1640, 20, 3040], [270,270,270,270]


#test
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'   
cxs, cys, radii = [300*5, 3000, 630*5], [230*5, 990, 2570], [200,200,200] 

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190516_Serum_10ugml_ada_10ul_NP/'
#cxs, cys, radii = [1075, 2580, 2515, 4100], [2140, 2130, 590, 2050], [330,330, 330, 330]
#
#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190509_Serum_1ugml_10mlNP/'
#cxs, cys, radii = [900, 1120, 2615, 3900, 4115], [640, 2110, 390*5, 240, 1780], [345,345,345,345,345]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_3ugml_10ulNP/'
#cxs, cys, radii = [1410, 2980, 1410, -80], [1435, 1370, -50, 1520], [325,325, 325,325]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190411_Output_Ada50ng_Live/'
#cxs, cys, radii = [1290, 2800, 2840, -245, -180, 4335], [790, 660, 450*5, 750, 2300, 680], [335,335,335, 335, 335,335]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_300ngml/'
#cxs, cys, radii = [720, 760, 2270, 3750, 3775], [930, 2530, 480*5, 173*5,2475], [260,260,260,260,260]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190430_Serum_NoAda_Control/'
#cxs, cys, radii = [], [], []

frame_numbers = []
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        frame_numbers.append(int(filename[6:].strip('.npy')))
frame_numbers.sort()

last_frame_file = 'Frame_'+str(frame_numbers[-1])+'.npy'
last_frame = np.load(in_dir+last_frame_file)

frame0_file = 'Frame_'+str(frame_numbers[0])+'.npy'
frame0  = np.load(in_dir+frame0_file)

frame1_file = 'Frame_'+str(len(frame_numbers)//3)+'.npy'
frame1 = np.load(in_dir+frame1_file)

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(last_frame, cmap='gray')
plt.show()

#display spot circles
#display = color.gray2rgb(last_frame)
#for cy, cx, radius in zip(cys, cxs, radii):
#    circy, circx = circle(cx, cy, radius, shape=(last_frame.shape[1], last_frame.shape[0]))
#    display[circx, circy] = (250, 20, 20)
#fig, ax = plt.subplots(figsize=(10,10))
#ax.imshow(display)
#plt.show()
#
#del display

mask = np.zeros_like(last_frame)
for cy, cx, radius in zip(cys, cxs, radii):
    circy, circx = circle(cx, cy, radius, shape=(last_frame.shape[1], last_frame.shape[0]))
    mask[circx,circy] = 255
    
plt.imshow(mask)

out_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/train/image/'

#imageio.imwrite(out_dir+'19.png', frame0)
#imageio.imwrite(out_dir+'19.png', frame1)
imageio.imwrite(out_dir+'test.png', last_frame)

out_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/train/label/'

imageio.imwrite(out_dir+'test.png', mask)
#imageio.imwrite(out_dir+'19.png', mask)
#imageio.imwrite(out_dir+'20.png', mask)







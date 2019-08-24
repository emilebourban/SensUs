# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:17:22 2019

@author: Emile
"""



import os
import matplotlib.pyplot as plt
import numpy as np
from skimage import color
from skimage.draw import circle_perimeter, circle

from skimage.filters import gaussian, threshold_minimum, threshold_otsu
from skimage.segmentation import find_boundaries, clear_border, mark_boundaries
from skimage.morphology import closing, opening, disk, dilation
from skimage.feature import canny
from skimage.transform import rescale, hough_circle, hough_circle_peaks

from utilities import smooth_background, find_circle

#intensity measurement  
#get average intensity for the circles selected and for the background as in image 2 in figure





    #TODO imagine a better method to select background. Here it was done when background hasn't been smoothed. 
    # What we do here is do a dilation of the detected foreground to prevent taking the sides of the circle and other artefacts
    # the foreground is selected by applying the same method as in detect_circle: rescaling, gaussian filtering and thresholding
    # 
    # Since it makes more sense to detect foreground in detect circle and in get_background_coord, maybe find a way to link them 
    # by calling to same funtion. => also better for redundancy
def get_background_coord(im, scaling_factor=None):
    '''
    Get coordinates of background points in the image after **insert method**
    '''
    #resize back to original size 
    if scaling_factor:
        im = rescale(im, int(1/scaling_factor))

    background_coord = []
    
    im = rescale(im, 0.2)
    im = gaussian(im, sigma=8)
    im = im < threshold_otsu(im)
    im = dilation(im, disk(im.shape[0]//20))
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if not im[i,j]:
                background_coord.append([i,j])
    
    if scaling_factor:
        #TODO think how to implement upscaling/resizing of background if needed
        pass
        #return np.array(background_coord)
    
    return np.array(background_coord)
    
def average_intensity(im, coords):
    '''
    Returns the average intensity of an image (im) over specific coordinates (coords)
    '''
    intensities = []
    for coord in coords:

        intensities.append(im[coord[0],coord[1]])
    return np.array(intensities[0]).mean()








###############################################################
# ça c'est utile pour tester la mesure d'intensité et le compte des particules:
# j'ai hardcodé la positions des spots et de zones du background pour chaque film


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
# cxs, cys, radii = [240, 555], [310, 295], [60,60]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
# cxs, cys, radii = [250, 555], [310, 330], [45,45]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'
# cxs, cys, radii = [300, 600, 630], [230, 200, 520], [35,35,30] #for 20190605_ada_8ugml_10ulNP
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190516_Serum_10ugml_ada_10ul_NP/'
# cxs, cys, radii = [210, 515, 500], [430, 425, 115], [60,60, 60]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190509_Serum_1ugml_10mlNP/'
# cxs, cys, radii = [180, 225, 520], [130, 425, 390], [60,60, 60]
# bxs, bys, bradii = [350,100, 700], [300,250,200], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_3ugml_10ulNP/'
# cxs, cys, radii = [280, 595], [283, 275], [60,60]
# bxs, bys, bradii = [450,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190411_Output_Ada50ng_Live/'
# cxs, cys, radii = [255, 560, 565], [155, 130, 450], [60,60,60]
# bxs, bys, bradii = [420,100, 700], [300,300,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_300ngml/'
# cxs, cys, radii = [143, 150, 450, 747, 753], [188, 507, 480, 173,489], [48,48,48,48,48]
# bxs, bys, bradii = [420,100, 700], [320,320,320], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190516_Serum_300ngml_ada_10ul_NP/'
# cxs, cys, radii = [143, 150, 450, 747, 753], [188, 507, 480, 173,489], [48,48,48,48,48]
# bxs, bys, bradii = [420,100, 700], [320,320,320], [80,70,70]


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190430_Serum_NoAda_Control/'
# cxs, cys, radii = [143, 150, 450, 747, 753], [188, 507, 480, 173,489], [48,48,48,48,48]
# bxs, bys, bradii = [420,100, 700], [320,320,320], [80,70,70]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190806 serum 10ug/ours/'
#cxs, cys, radii = [40, 200, 360,520], [110, 110, 120, 130], [30,30,30,30]
#bxs, bys, bradii = [120,280, 450], [175,200,220], [60,60,60]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190806 serum 10ug/ours/apres35min/'
#cxs, cys, radii = [190,190], [185,185], [110,10]
#bxs, bys, bradii = [450,450, 62], [65,300,340], [60,60,60]

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190807plasma10ugbelushkin/'
#cxs, cys, radii = [250,540], [410,390], [40,40]
#bxs, bys, bradii = [110,400], [110,110], [100,100]

in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190807plasma10ugAfter1h/'
cxs, cys, radii = [125, 140, 300, 445, 460, 470], [340, 195, 190, 370,210,55], [25,25,25,25,25,25]
bxs, bys, bradii = [220,380], [110,110], [70,70]

scale= 0.2


#Sorting files names 
frame_numbers = []
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        frame_numbers.append(int(filename[6:].strip('.npy')))
frame_numbers.sort()

last_frame_file = 'Frame_'+str(frame_numbers[-1])+'.npy'
last_frame = np.load(in_dir+last_frame_file)


#downscale image by 5, might be removed/changed later
last_frame = rescale(last_frame, scale)#, anti_aliasing=True, anti_aliasing_sigma=2)
fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(last_frame, cmap='gray')
plt.show()
#background = get_background_coord(last_frame)

mask = np.zeros_like(last_frame)
for cx, cy, radius in zip(bxs, bys, bradii):
    disk = circle(cy,cx,radius, shape=last_frame.shape)
    mask[disk] = 1

background = np.array(np.nonzero(mask)).T

#display background circles
display = color.gray2rgb(last_frame)
for cy, cx, radius in zip(bys, bxs, bradii):
    circy, circx = circle_perimeter(cx, cy, radius)
    display[circx, circy] = (250, 20, 20)
fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(display, cmap='gray')
plt.show()
del display

#display spot circles
display = color.gray2rgb(last_frame)
for cy, cx, radius in zip(cys, cxs, radii):
    circy, circx = circle_perimeter(cx, cy, radius)
    display[circx, circy] = (250, 20, 20)

fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(display, cmap='gray')
plt.show()

del display

# get coordinates of points in spots
disks=[]
for cy, cx, radius in zip(cys, cxs, radii):
    disks.append(circle(cy, cx, radius, shape = last_frame.shape))
print('DISK SHAPE ', disks)
#TODO research how to free up memory. del may not be satisfactory. Maybe a "with" statement.


del last_frame

intensity_back = []
intensity_spot = []
intensity_back_s = []
intensity_spot_s = []

for num in frame_numbers:
    
    frame_file = 'Frame_'+str(num)+'.npy'
    print(frame_file)
    frame = np.load(in_dir+frame_file)
    frame = color.rgb2gray(frame)
    frame_s = smooth_background(frame)

    frame_s = rescale(frame_s, scale)
    intensity_spot_s.append(average_intensity(frame_s, disks))
    intensity_back_s.append(average_intensity(frame_s, background))

    intensity_spot.append(average_intensity(frame, disks))
    intensity_back.append(average_intensity(frame, background))
    del frame
    del frame_s

intensity_back = np.array(intensity_back)
intensity_spot = np.array(intensity_spot)

intensity_back_s = np.array(intensity_back_s)
intensity_spot_s = np.array(intensity_spot_s)

np.save(in_dir+'int/int_back_smoothed',intensity_back_s)
np.save(in_dir+'int/int_spot_smoothed',intensity_spot_s)

np.save(in_dir+'int/int_back',intensity_back)
np.save(in_dir+'int/int_spot',intensity_spot)





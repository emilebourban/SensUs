# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 16:04:36 2019

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
    return np.array(intensities).mean()



def get_intensities(in_dir, scale=0.2, smoothing=True):
    '''
    
    '''
    #Sorting files names
    #TODO adapt to new filenames if needed
    frame_numbers = []
    for filename in os.listdir(in_dir):
        if filename.endswith(".npy"):
            frame_numbers.append(int(filename[6:].strip('.npy')))
    frame_numbers.sort()

    #Load last frame to find spot / background region on it
    last_frame_file = 'Frame_'+str(frame_numbers[-1])+'.npy'
    last_frame = np.load(in_dir+last_frame_file)
    #downscale image by 5, might be removed/changed later
    last_frame = rescale(last_frame, scale, anti_aliasing=True)
    
    background = get_background_coord(last_frame)
    
    cxs, cys, radii = find_circle(last_frame)


#test count particles


#TODO: remove this later, this is just for checking that the circle found are correct
    display = color.gray2rgb(last_frame)
    for cy, cx, radius in zip(cys, cxs, radii):
        circy, circx = circle_perimeter(cx, cy, radius)
        display[circx, circy] = (250, 20, 20)
    print(display.shape)
    plt.imshow(display)
    plt.show()
    del display

    # get coordinates of points in spots
    disks=[]
    for cy, cx, radius in zip(cys, cxs, radii):
        disks.append(circle(cy, cx, radius, shape = last_frame.shape))
    #TODO research how to free up memory. del may not be satisfactory. Maybe a "with" statement
    disks = np.concatenate(disks, axis =1)

    del last_frame

    intensity_back = []
    intensity_spot = []

    #iterate over each frame in the movie and gets the intensity in spot and background
    for num in frame_numbers:
        frame_file = 'Frame_'+str(num)+'.npy'
        print(frame_file)
        frame = np.load(in_dir+frame_file)
        if smoothing:
            frame = smooth_background(frame)
        frame = rescale(frame, scale, anti_aliasing=True)
        intensity_spot.append(average_intensity(frame, disks))
        intensity_back.append(average_intensity(frame, background))
        del frame
    
    return np.array(intensity_back), np.array(intensity_spot)


    
    
#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190509_Serum_1ugml_10mlNP/'
#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_3ugml_10ulNP/'
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190411_Output_Ada50ng_Live/'


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'



intensity_back, intensity_spot = get_intensities(in_dir, scale=0.1)
y = (intensity_back - intensity_spot)/(intensity_back+intensity_spot)
timescale = np.arange(0, y.shape[0]/2, 0.5)

plt.plot(timescale, y)



#in_dir2 = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
#
#intensity_back2, intensity_spot2 = get_intensities(in_dir2, scale=0.2)
#diff2 = (intensity_back2 - intensity_spot2)/(intensity_back2+intensity_spot2)
#timescale2 = np.arange(0, diff2.shape[0]/2, 0.5)

#plt.plot(timescale2, diff2)



#in_dir3 = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'
#
#intensity_back3, intensity_spot3 = get_intensities(in_dir3, scale=0.2)
#diff3 = (intensity_back3 - intensity_spot3)/(intensity_back3 + intensity_spot3)
#timescale3 = np.arange(0, diff3.shape[0]/2, 0.5)
#
#plt.plot(timescale3, diff3)












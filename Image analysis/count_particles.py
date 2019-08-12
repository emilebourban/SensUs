# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:26:47 2019

@author: Emile
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import circle, circle_perimeter
from skimage import color
from skimage.filters import gaussian, threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import closing, opening, disk, dilation


def count_particles(im, cxs, cys, radii):
    '''

    Parameters
    ----------
    im : array
        image.
    rois : tuple or list
        contains center coordinate and radius (cx, cy, rad)

    Returns
    -------
    ccs : regionprops
        description

    '''
    threshold = 0
    #calculate threshold on squares inside the circular ROI
    for cx, cy, radius in zip(cxs, cys, radii):
        x = int(radius*np.sqrt(2)/2)
        y = int(radius*np.sqrt(2)/2)
        threshold += threshold_otsu(im[cy-y:cy+y,cx-x:cx+x])
    threshold /= len(radii)

    #TODO add case for background if we also want to count particles there

    #creating a mask in order to only select the spots
    mask = np.zeros_like(im)
    for cx, cy, radius in zip(cxs, cys, radii):
        disk = circle(cy,cx,radius, shape=im.shape)
        mask[disk] = 1

    # the background in the mask will be in the background => only keeps the points higher than threshold that are in  the spot
    im = (mask*im)> threshold

    # #plotting to assess quality of thresholding
    # fig, ax = plt.subplots(figsize=(30,30))
    # ax.imshow(im)

    #opening allows to separate some of the foreground areas that are fused together
    #TODO optimize opening structuring elemt size/ shape
    im = opening(im)

    #labels the different connected component region in the foreground
    labeled = label(im)

    #gets region properties of each labeled region
    ccs = regionprops(labeled, im)

    #TODO make list of binary_cc (keep some kind of absolute coordinates to pass between images) !might take ram if need to load multiple images
    #take care that background mask (if circle roi) is removed as well
    
    #TODO adapt filter size. 8 - 80 pixels in original from ludo
    count=0
    for cc in ccs:

        if cc.area <= 80 and cc.area >= 8:
            count += 1
            #ccs.remove(cc) this works but waaaaay too long. if we need to store other quantities (e.g. intensity), make a new list instead of passing the whole regionprops

        #TODO try to filter by shape
    #TODO try to filter by intensity

    #TODO adapt if needed to give coordinate / intensity /other
    return count


# THIS IS USEFUL FOR COUNTING PARTICLES / MEASURE INTENSITY
# cxs, cys, radii are the spots coordinates in the images in in_dir
# bxs, bys, bradii are the coordinates of circles of background
# they were harcoded here for testing, but later we need to find spots / background regions automatically

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
# cxs, cys, radii = [240*5, 555*5], [310*5, 295*5], [60*5,60*5]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
# cxs, cys, radii = [250*5, 555*5], [310*5, 330*5], [45*5,45*5]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'
# cxs, cys, radii = [300*5, 600*5], [230*5, 200*5], [35*5,35*5] #for 20190605_ada_8ugml_10ulNP
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190516_Serum_10ugml_ada_10ul_NP/'
# cxs, cys, radii = [210*5, 515*5, 500*5], [430*5, 425*5, 115*5], [60*5,60*5, 60*5]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190509_Serum_1ugml_10mlNP/'
cxs, cys, radii = [180*5, 225*5, 520*5], [130*5, 425*5, 390*5], [60*5,60*5, 60*5]
bxs, bys, bradii = [350,100, 700], [300,250,200], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_3ugml_10ulNP/'
# cxs, cys, radii = [280*5, 595*5], [283*5, 275*5], [60*5,60*5]
# bxs, bys, bradii = [450,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190411_Output_Ada50ng_Live/'
# cxs, cys, radii = [255*5, 560*5, 565*5], [155*5, 130*5, 450*5], [60*5,60*5,60*5]
# bxs, bys, bradii = [420,100, 700], [300,300,150], [80,70,70]



im = np.load(in_dir+'Frame_110.npy')
plt.imshow(im)
plt.show()
# display = color.gray2rgb(im)
# for cy, cx, radius in zip(cys, cxs, radii):
#     circy, circx = circle_perimeter(cx, cy, radius)
#     display[circx, circy] = (250, 20, 20)
# plt.imshow(display)
# plt.show()
# del display

x = count_particles(im, cxs, cys, radii)

import os
frame_numbers = []
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        frame_numbers.append(int(filename[6:].strip('.npy')))
frame_numbers.sort()

count=[]
for num in frame_numbers:
    frame_file = 'Frame_'+str(num)+'.npy'
    print(frame_file)
    frame = np.load(in_dir+frame_file)
    count.append(count_particles(frame, cxs, cys, radii))
    del frame










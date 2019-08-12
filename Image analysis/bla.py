# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:02:32 2019

@author: Emile
"""

from utilities import smooth_background
import matplotlib.pyplot as plt
import numpy as np


#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'


from skimage import data, color
from skimage.draw import circle_perimeter
from skimage.filters import gaussian, threshold_minimum, threshold_otsu
from skimage.segmentation import find_boundaries, clear_border, mark_boundaries
from skimage.morphology import closing, opening, disk, dilation
from skimage.feature import canny
from skimage.transform import rescale, hough_circle, hough_circle_peaks

im = np.load(in_dir+'Frame_110.npy')

im0 = smooth_background(im)
im1 = rescale(im0,0.2)
im2 = gaussian(im1, sigma=8)

im3 = im2 < threshold_otsu(im2)
# 4, 6 for frame > 80
plt.imshow(im, cmap='gray')
im4 = closing(opening(im3, selem=disk(8)),selem=disk(12))
#im4 = opening(closing(im3, selem=disk(6)),selem=disk(4))
edges = canny(im4)


# Detect two radii

hough_radii = np.arange(im4.shape[0]//12, im4.shape[0]//8, 1)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 5 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=2)

# Draw them
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 10))

#plot filtered and rescaled
ax[0,0].imshow(im2, cmap=plt.cm.gray)
#plot result of morphologicla operations
ax[0,1].imshow(im4)

#plot edges
ax[1,0].imshow(edges)

#plot hough circles 
im2 = color.gray2rgb(im2)

for center_y, center_x, radius in zip(cy, cx, radii):
    print('hello')
    circy, circx = circle_perimeter(center_y, center_x, radius)
    im2[circy, circx] = (250, 20, 20)
    
ax[1,1].imshow(im2)
plt.show()
#%%
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'

im_10 = np.load(in_dir+'Frame_2.npy')

plt.imshow(im_10, cmap='gray')

#%%
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'

im_180 = np.load(in_dir+'Frame_110.npy')

plt.imshow(im_180, cmap='gray')

#%%
test2 = gaussian(im_180-im_10,4)
plt.imshow(gaussian(im_180-im_10,4), cmap='gray')


#%%

#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'

first = smooth_background(np.load(in_dir+'Frame_2.npy'))
last = np.load(in_dir+'Frame_110.npy')


first = rescale(first,0.2)
last = rescale(last,0.2)

im1 = last
im2 = gaussian(im1, sigma=8)

im3 = im2 < threshold_otsu(im2)
# 4, 6 for frame > 80
plt.imshow(im1, cmap='gray')
im4 = closing(opening(im3, selem=disk(8)),selem=disk(12))
#im4 = opening(closing(im3, selem=disk(6)),selem=disk(4))
edges = canny(im4)


# Detect two radii

hough_radii = np.arange(im4.shape[0]//12, im4.shape[0]//8, 1)
hough_res = hough_circle(edges, hough_radii)

# Select the most prominent 5 circles
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=2)


# Draw them
fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(10, 10))

#plot filtered and rescaled
ax[0,0].imshow(im2, cmap=plt.cm.gray)
#plot result of morphologicla operations
ax[0,1].imshow(im4)

#plot edges
ax[1,0].imshow(edges)

#plot hough circles 
im2 = color.gray2rgb(im2)

for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    im2[circy, circx] = (250, 20, 20)
    
ax[1,1].imshow(im2)
plt.show()




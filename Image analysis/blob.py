# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:05:50 2019

@author: Emile
"""

import numpy as np
import matplotlib.pyplot as plt
import measure_intensity


from skimage.exposure import histogram
from skimage.morphology import closing, opening, disk, dilation
from utilities import smooth_background
from count_particles import count_particles
from skimage.filters import gabor, gaussian, threshold_minimum, threshold_otsu, threshold_li, threshold_yen, try_all_threshold
mat= np.array([[1,2,3],[4,5,6],[7,8,9]])
a=[0,1,1]
b=[0,0,2]
mat[a,b]
c=(a,b)
print(mat[c])


in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190418_Ada_Serum10times_10ugml/'
cxs, cys, radii = [240*5, 555*5], [310*5, 295*5], [60*5,60*5]
# bxs, bys, bradii = [400,100, 700], [300,150,150], [80,70,70]

# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190502_Ada_3ug_serum10p/'


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_8ugml_10ulNP/'


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190516_Serum_10ugml_ada_10ul_NP/'


#in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190509_Serum_1ugml_10mlNP/'


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190605_ada_3ugml_10ulNP/'


# in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190411_Output_Ada50ng_Live/'

im1 = np.load(in_dir+'Frame_10.npy')
im2 = np.load(in_dir+'Frame_100.npy')

im2 = smooth_background(im2)


plt.imshow(im2)
plt.show()




















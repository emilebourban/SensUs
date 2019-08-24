# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:58:19 2019

@author: Emile
"""


import os 
#directory = r'D:\Utilisateurs\Emile\Documents\MA2\SensUs\data\train\label' 
#for filename in os.listdir(directory):
#    prefix = filename.split(".jpg")[0]
#    print(filename)
#    os.rename(directory+'\\'+filename, directory+prefix+".png")
    
    
    
import numpy as np
import matplotlib
in_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190806 serum 10ug/belush/'
for filename in os.listdir(in_dir):
    if filename.endswith(".npy"):
        array =  np.load(in_dir+filename)
        matplotlib.image.imsave(in_dir+filename[:-4]+'.png', array, cmap='gray')
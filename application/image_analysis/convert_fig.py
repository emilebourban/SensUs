# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:43:38 2019

@author: Emile
"""
import os
import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

def fig_to_bmp(in_dir, out_dir):
    '''
    Converts all the .fig matlab images from in_dir to NumPy format (.npy) and saves them in out_dir
    '''
    for filename in os.listdir(in_dir):
        if filename.endswith(".fig"):
            print(filename)
            fig = loadmat(in_dir+filename,squeeze_me=False, struct_as_record=False)
            try:
                im = fig['hgS_070000'][0,0].children[0,0].children[0,0].properties[0,0].CData
                np.save(out_dir+filename[:-4], im)
            except IndexError:
                print('Error for '+filename)
                continue
            
        else:
            continue
        
def tif_to_bmp(in_dir, out_dir):
    '''
    Converts all the .fig matlab images from in_dir to NumPy format (.npy) and saves them in out_dir
    '''
    for filename in os.listdir(in_dir):
        if filename.endswith(".tif"):
            print(filename[:-8]+str(int(filename[6:-4])))
            im = plt.imread(in_dir+filename)
            np.save(out_dir+filename[:-8]+str(int(filename[6:-4])), im)
            
        else:
            continue
        
in_dir = 'E:/Sensus/test/20190807plasma/'
out_dir = 'D:/Utilisateurs/Emile/Documents/MA2/SensUs/data/20190807plasma10ugAfter1h/'

tif_to_bmp(in_dir, out_dir)
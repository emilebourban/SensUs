# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 19:00:08 2019

@author: Emile
"""


import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import rescale
from skimage.feature import peak_local_max
from numpy.polynomial import polynomial
from numpy.polynomial.polynomial import polyval2d



#%%Background smoothing functions

def polyfit2d(x, y, f, deg):
    '''
    Fits a 2d polynomyial of degree deg to the points f where f is the value of point [x,y]
    '''
    x = np.asarray(x)
    y = np.asarray(y)
    f = np.asarray(f)
    deg = np.asarray(deg)
    vander = polynomial.polyvander2d(x, y, deg)
    vander = vander.reshape((-1,vander.shape[-1]))
    f = f.reshape((vander.shape[0],))
    c = np.linalg.lstsq(vander, f, rcond=None)[0]
    return c.reshape(deg+1)

def smooth_background(img, rescale_factor=0.1, poly_deg=[2,2]):
    '''
    Smooths the background of the image by modeling the background with a polynomial 
    surface by regression on the local maximum intensity peaks and dividing the original
    image by this surface.

    Parameters
    ----------
    img : ndarray
        Image.
    rescale_factor : float or int, optional
        The scaling of the image used to fit the polynomial surface. The default is 0.1.
    poly_deg : list or double, optional
        List where the first and secong elements are the polynomial degrees on the x and y axis respectively. The default is [1,2].

    Returns
    -------
    the input image with smoothed background.

    '''

    imgs = rescale(img, rescale_factor, preserve_range=True)
    BW = peak_local_max(imgs, indices=False)
    k = BW*imgs
    
    ind = np.nonzero(k)
    z = k[ind]
    
#TODO watch out polynomial degree might change depending on background. We chose [1, 2], because deformation looked "cylindrical"
#   but [2, 2] or other could make sense depending on deformation.
    p = polyfit2d(ind[0],ind[1],z, poly_deg)
    xx, yy = np.meshgrid(np.linspace(0, imgs.shape[0], img.shape[0]), 
                         np.linspace(0, imgs.shape[1], img.shape[1]))

    background = np.transpose(polyval2d(xx, yy, p))
    return background

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:21:22 2019

@author: Emile
"""

import pygame
from . import pyspin_cam as pc
import numpy as np

class Capture(object):
    def __init__(self):
        
        self.size = (800,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)


        self.cam = pc.Camera()
#        self.cam.buffer_newest_first()
        self.cam['StreamBufferHandlingMode'].value = 'NewestFirst'
        
        #Setting framerate to maximum
        self.cam['TriggerMode'].value = 'Off'
        self.cam['AcquisitionFrameRateEnable'].value = True
        self.cam['AcquisitionFrameRate'].value = self.cam['AcquisitionFrameRate'].max
        
#        self.cam['AcquisitionMode'].value = 'Continuous'
        
        #binning of the image for smaller image size => higher framerate
        self.cam['DecimationSelector'].value = 'All'
        self.cam['BinningHorizontal'].value = 4
        self.cam['BinningVertical'].value = 4
        self.cam['BinningHorizontalMode'].value = 'Average'
        self.cam['BinningVerticalMode'].value = 'Average'

        #setting pixel format
        self.cam['PixelFormat'].value = 'Mono8'
        
        #TODO give size to constructor depending on window size
        self.cam['Width'].value = self.size[0]
        self.cam['Height'].value = self.size[1]

        self.cam.BeginAcquisition()
        
        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)

    def get_and_flip(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        
        #de array a surfacepygame
        image = self.cam.GetNextImage()
        if image.IsIncomplete():
            print('Image incomplete with image status %d...' % image.GetImageStatus())

        else:
            h = image.GetHeight()
            w = image.GetWidth()
            numChannels = image.GetNumChannels()
            if numChannels > 1:
                array = image.GetData().reshape(h, w, numChannels)
            else:               
                array = image.GetData().reshape(h, w).T
                array = array[..., np.newaxis].repeat(3, -1).astype("uint8")
        self.snapshot = pygame.pixelcopy.make_surface(array)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.update()

    def release(self):         
        self.cam.release()
        
    def __del__(self):
        self.release()
        

    def draw(self):
        pass



























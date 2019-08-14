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

        # this is the same as what we saw before
#        self.clist = pygame.camera.list_cameras()
#        if not self.clist:
#            raise ValueError("Sorry, no cameras detected.")
#        self.cam = pygame.camera.Camera(self.clist[0], self.size)
#        self.cam.start()
        
        self.cam = pc.Camera()
        self.cam.buffer_newest_first()
        self.cam.set_max_framerate()
#        self.cam['AcquisitionMode'].value = 'Continuous'
        #TODO set the size of acquired image
        #set exposure
#        self.cam[]
        
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
                ret = image.GetData().reshape(h, w)
                array = np.empty((h,w,3),dtype=np.uint8)
                array[:,:,2]=array[:,:,1]=array[:,:,0]=ret
        self.snapshot = pygame.pixelcopy.make_surface(array)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        pygame.display.update()

    def release(self):         
        self.cam.release()
        
    def __del__(self):
        self.release()
        
    def run(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    # close the camera safely
#                    self.quitting = True
                    going = False
#                    pygame.display.quit()
                    self.release()
                    pygame.quit()
#                    import sys
#                    sys.exit()
            self.get_and_flip()
        






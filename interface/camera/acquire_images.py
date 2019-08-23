# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 11:25:59 2019

@author: Emile
"""
import os
import PySpin
import time
from datetime import datetime
#TODO correct the path
from camera import pyspin_cam as pc


class Capture(object):
    
    def __init__(self):
        
        self.cam = pc.Camera()

        #setting pixel format
        self.cam['PixelFormat'].value = 'Mono8'
        self.cam['AcquisitionMode'].value = 'Continuous'
        #TODO give size to constructor depending on window size
        self.cam['Width'].value = self.cam['Width'].max
        self.cam['Height'].value = self.cam['Height'].max
        self.cam['GainAuto'].value = 'Once'
        self.cam['ExposureAuto'].value = 'Once'
        
        
        self.cam['ChunkModeActive'].value = True
        for chunk in self.cam['ChunkSelector'].content:
            print(chunk.split(sep='_')[-1])
            
            self.cam['ChunkSelector'].value = chunk.split(sep='_')[-1]
            self.cam['ChunkEnable'].value = True
            
        print(self.cam['ChunkSelector'].content)

        self.cam.BeginAcquisition()
        
        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.

    def get_image(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        
        #de array a surfacepygame
        image = self.cam.GetNextImage()
        if image.IsIncomplete():
            print('Image incomplete with image status %d...' % image.GetImageStatus())
            image.Release()
            return 
        else:
            # Convert image to Mono8
            image_converted = image.Convert(PySpin.PixelFormat_Mono8)
                    
            chunk_data = image.GetChunkData()
    
            # Retrieve exposure time (recorded in microseconds)
            exposure_time = chunk_data.GetExposureTime()
            print('\tExposure time: {}'.format(exposure_time))
    
            # Retrieve frame ID
            frame_id = chunk_data.GetFrameID()
            print('\tFrame ID: {}'.format(frame_id))
    
            # Retrieve gain; gain recorded in decibels
            gain = chunk_data.GetGain()
            print('\tGain: {}'.format(gain))
            
            # Retrieve black level;
            BL = chunk_data.GetBlackLevel()
            print('\tBlack Level: {}'.format(BL))
            
            
            image.Release()
            return image_converted
        
        
        
    def release(self):         
        self.cam.release()
        
    def __del__(self):
        self.release()
        

    def draw(self):
        pass


def main():
    """
    Example entry point; please see Enumeration example for more in-depth
    comments on preparing and cleaning up the system.

    :return: True if successful, False otherwise.
    :rtype: bool
    """

    # Since this application saves images in the current folder
    # we must ensure that we have permission to write to this folder.
    # If we do not have permission, fail right away.
    try:
        test_file = open('test.txt', 'w+')
    except IOError:
        print('Unable to write to current directory. Please check permissions.')
        input('Press Enter to exit...')
        return False
    test_file.close()
    os.remove(test_file.name)
    capture = Capture()
    
    save_dir=''


        

    #Starts iteration to set the gain and exposure time
    for i in range(100):
        
        im = capture.get_image()
        chunk_data = im.GetChunkData()

        # Retrieve exposure time (recorded in microseconds)
        exposure_time = chunk_data.GetExposureTime()
        print('\tExposure time: {}'.format(exposure_time))

        # Retrieve frame ID
        frame_id = chunk_data.GetFrameID()
        print('\tFrame ID: {}'.format(frame_id))

        # Retrieve gain; gain recorded in decibels
        gain = chunk_data.GetGain()
        print('\tGain: {}'.format(gain))
        
        # Retrieve black level;
        BL = chunk_data.GetBlackLevel()
        print('\tBlack Level: {}'.format(BL))
        
    
    num_images = 120
    for i in range(num_images):
         # Create a unique filename
        filename = 'Frame_'+'0'*(4 - len(str(i)))+str(i)+'.tif' 
        im = capture.get_image()
        

        
        
        print(datetime.now())
        time.sleep(30)
        # Save image
        im.Save(save_dir+filename)
        print('Saved image '+filename)
        
    del capture

    input('Done! Press Enter to exit...')
    return

if __name__ == '__main__':
    main()

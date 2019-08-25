from camera import Camera
import PySpin as spin
import numpy as np


class Acquistion:
    def __init__(self):
        self.cam = Camera()
        
    def BeginAcquisition(self):
        self.cam.BeginAcquisition()      
        
    def get_image():
        pass
    
    def __del__(self):
        del self.cam


class Capture(Acquistion):    
    def __init__(self):
        super().__init__(self)
        self.cam['StreamBufferHandlingMode'].value = 'NewestOnly'

        self.cam['PixelFormat'].value = 'Mono8'
        self.cam['AcquisitionMode'].value = 'Continuous'
        self.cam['StreamCRCCheckEnable'].value = True

        #TODO give size to constructor depending on window size
        self.cam['Width'].value = self.cam['Width'].max
        self.cam['Height'].value = self.cam['Height'].max
        self.cam['GainAuto'].value = 'Off'
        self.cam['Gain'].value= 0
        self.cam['AutoExposureExposureTimeUpperLimit'].value = 50000
        self.cam['ExposureAuto'].value = 'Once'

        self.BeginAcquisition()
        
    def get_image(self, exposure_setting=False):
        image = self.cam.GetNextImage()
        if image.IsIncomplete():
            print('Image incomplete with image status %d...' % image.GetImageStatus())
            image.Release()
            return 
        else:
            # Convert image to Mono8
            image_converted = image.Convert(spin.PixelFormat_Mono8)

            image.Release()
            return image_converted
    
    def set_exposure_time(self):
        self.cam['ExposureAuto'].value = 'Once'

        for i in range(50):
            im = self.get_image()
            chunk_data = im.GetChunkData()
            im.Release()
            
        self.cam['ExposureAuto'].value = 'Off'
        self.cam['ExposureTime'].value = chunk_data.GetExposureTime()        
        

    
class LiveStream(Acquistion):
    def __init__(self):
        super().__init__(self)
        
        self.cam['StreamBufferHandlingMode'].value = 'NewestFirst'
        self.cam['TriggerMode'].value = 'Off'
        self.cam['AcquisitionFrameRateEnable'].value = True
        self.cam['AcquisitionFrameRate'].value = self.cam['AcquisitionFrameRate'].max
        self.cam['StreamCRCCheckEnable'].value = False
        self.cam['AcquisitionMode'].value = 'Continuous'
        self.cam['DecimationSelector'].value = 'All'
        self.cam['BinningHorizontal'].value = 4
        self.cam['BinningVertical'].value = 4
        self.cam['BinningHorizontalMode'].value = 'Average'
        self.cam['BinningVerticalMode'].value = 'Average'
        self.cam['PixelFormat'].value = 'Mono8'
        self.cam['GainAuto'].value = 'Off'
        self.cam['Gain'].value= 0        
        self.cam['AutoExposureExposureTimeUpperLimit'].value = 50000
        self.cam['ExposureAuto'].value = 'Once'
        #TODO take smaller part of image if lagging
        self.cam['Width'].value = self.cam['Width'].max
        self.cam['Height'].value = self.cam['Height'].max
        
        self.BeginAcquisition()
        
    def get_image(self):
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
        
        image.Release()

        return pygame.pixelcopy.make_surface(array)

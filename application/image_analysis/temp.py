# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:20:02 2019

@author: Emile
"""
import PySpin
#import cv2


def getNumCameras():
    system = PySpin.System.GetInstance()
    numCameras = len(system.GetCameras())
    system.ReleaseInstance()
    return numCameras


class PySpinCapture:


    def __init__(self, index, width=None, height=None, x_offset=None, y_offset=None, binningRadius=4):

        self._system = PySpin.System.GetInstance()

        self._cameraList = self._system.GetCameras()

        self._camera = self._cameraList.GetByIndex(index)
        self._camera.Init()

        self._nodemap = self._camera.GetNodeMap()


        # Enable continuous acquisition mode.
        nodeAcquisitionMode = PySpin.CEnumerationPtr(
                self._nodemap.GetNode('AcquisitionMode'))
        nodeAcquisitionModeContinuous = \
                nodeAcquisitionMode.GetEntryByName(
                        'Continuous')
        acquisitionModeContinuous = \
                nodeAcquisitionModeContinuous.GetValue()
        nodeAcquisitionMode.SetIntValue(
                acquisitionModeContinuous)
        


    
        # Set the vertical binning radius.
        # The horizontal binning radius is automatically set
        # to the same value.
        nodeBinningVertical = PySpin.CIntegerPtr(
                self._nodemap.GetNode('BinningVertical'))
        nodeBinningVertical.SetValue(binningRadius)

        # Set the ROI.
#        x, y, w, h  = roi
#
#        nodeOffsetX = PySpin.CIntegerPtr(
#                self._nodemap.GetNode('OffsetX'))
#        nodeOffsetX.SetValue(x)
#        nodeOffsetY = PySpin.CIntegerPtr(
#                self._nodemap.GetNode('OffsetY'))
#        nodeOffsetY.SetValue(y)
#        nodeWidth = PySpin.CIntegerPtr(
#                self._nodemap.GetNode('Width'))
#        nodeWidth.SetValue(nodeWidth.GetMax())
#        nodeHeight = PySpin.CIntegerPtr(
#                self._nodemap.GetNode('Height'))
#        nodeHeight.SetValue(nodeHeight.GetMax())
#
        self._camera.BeginAcquisition()


#    def get(self, propId):
#        if propId == cv2.CAP_PROP_FRAME_WIDTH:
#            nodeWidth = PySpin.CIntegerPtr(
#                    self._nodemap.GetNode('Width'))
#            return float(nodeWidth.GetValue())
#        if propId == cv2.CAP_PROP_FRAME_HEIGHT:
#            nodeHeight = PySpin.CIntegerPtr(
#                    self._nodemap.GetNode('Height'))
#            return float(nodeHeight.GetValue())
#        return 0.0

    def configure_pixel_format(self, pixel_format='Mono8'):
        try:
            result = True
    
            # Retrieve the enumeration node from the nodemap
            node_pixel_format = PySpin.CEnumerationPtr(self._nodemap.GetNode('PixelFormat'))
            if PySpin.IsAvailable(node_pixel_format) and PySpin.IsWritable(node_pixel_format):
    
                # Retrieve the desired entry node from the enumeration node
                # *** NOTE *** for the pixel_format parameter, see spinnaker doc
                node_pixel_format_new = PySpin.CEnumEntryPtr(node_pixel_format.GetEntryByName(pixel_format))
                if PySpin.IsAvailable(node_pixel_format_new) and PySpin.IsReadable(node_pixel_format_new):
    
                    # Retrieve the integer value from the entry node
                    pixel_format_new = node_pixel_format_new.GetValue()
    
                    # Set integer as new value for enumeration node
                    node_pixel_format.SetIntValue(pixel_format_new)
    
                    print('Pixel format set to %s...' % node_pixel_format.GetCurrentEntry().GetSymbolic())
    
                else:
                    print('Pixel format ' + pixel_format + ' not available...')
    
            else:
                print('Pixel format not available...')
                
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False
        
        return result

    def configure_image_dimensions(self, width=None, height=None, x_offset=None, y_offset=None):
        """
        Configures a number of settings on the camera including offsets  X and Y, width,
        height, and pixel format. These settings must be applied before BeginAcquisition()
        is called; otherwise, they will be read only. Also, it is important to note that
        settings are applied immediately. This means if you plan to reduce the width and
        move the x offset accordingly, you need to apply such changes in the appropriate order.
    
        :param nodemap: GenICam nodemap.
        :type nodemap: INodeMap
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        print('\n*** CONFIGURING CUSTOM IMAGE SETTINGS *** \n')
    
        try:
            result = True
    
            # Apply minimum to offset X
            if x_offset:
                node_offset_x = PySpin.CIntegerPtr(self._nodemap.GetNode('OffsetX'))
                if PySpin.IsAvailable(node_offset_x) and PySpin.IsWritable(node_offset_x):
                    
                    if x_offset >= node_offset_x.GetMin() and x_offset <= node_offset_x.GetMin():
                        node_offset_x.SetValue(x_offset)
                        print('Offset X set to %i...' % x_offset)
                    else:  
                        print('X offset value out of range')
                        
                    
                else:
                    print('Offset X not available...')
    
            # Apply minimum to offset Y
            if y_offset:
                node_offset_y = PySpin.CIntegerPtr(self._nodemap.GetNode('OffsetY'))
                if PySpin.IsAvailable(node_offset_y) and PySpin.IsWritable(node_offset_y):
                    
                    if y_offset >= node_offset_y.GetMin() and y_offset <= node_offset_y.GetMin():
                        node_offset_x.SetValue(y_offset)
                        print('Offset Y set to %i...' % y_offset)
                    else:  
                        print('Y offset value out of range')
                    
        
                else:
                    print('Offset Y not available...')
    
    
            # Set maximum width   
            if width:
                node_width = PySpin.CIntegerPtr(self._nodemap.GetNode('Width'))
                if PySpin.IsAvailable(node_width) and PySpin.IsWritable(node_width):
                    inc = node_width.GetInc()
                
                    if width%inc == 0 and width <= node_width.GetMax() and width >= node_width.GetMin():
                        node_width.SetValue(width)
                        print('Width set to %i...' % width)
                    else:
                        print('Value error width')
                    
                else:
                    print('Width not available...')
                
                
    #             Set maximum height   
            if height:
                node_height = PySpin.CIntegerPtr(self._nodemap.GetNode('Height'))
                if PySpin.IsAvailable(node_height) and PySpin.IsWritable(node_height):
                    inc = node_height.GetInc()
                
                    if height%inc == 0 and height <= node_height.GetMax() and height >= node_height.GetMin():
                        node_height.SetValue(height)
                        print('Height set to %i...' % height)
                    else:
                        print('Value error height')
                    
                else:
                    print('Height not available...')
    
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False
    
        return result
    

    def __del__(self):
        self.release()

    def configure_exposure(self, mode='continuous', exposure_time=2000000.0):
        """
         This function configures a custom exposure time. Automatic exposure is turned
         off in order to allow for the customization, and then the custom setting is
         applied.
    
         :param cam: Camera to configure exposure for.
         :type cam: CameraPtr
         :return: True if successful, False otherwise.
         :rtype: bool
        """
    
        print('*** CONFIGURING EXPOSURE ***\n')
    
        try:
            result = True
    
            if self._camera.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to disable automatic exposure. Aborting...')
                return False
            
            if mode=='manual':
                self._camera.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
                print('Automatic exposure disabled...')
        
                if self._camera.ExposureTime.GetAccessMode() != PySpin.RW:
                    print('Unable to set exposure time. Aborting...')
                    return False
        
                # Ensure desired exposure time does not exceed the maximum
                exposure_time_to_set = exposure_time
                if exposure_time_to_set >= self._camera.ExposureTime.GetMax():
                    print('Exposure time of {} exceeds maximal possible value'.format(exposure_time_to_set))
                    exposure_time_to_set = self._camera.ExposureTime.GetMax()
                    
                self._camera.ExposureTime.SetValue(exposure_time_to_set)
                print('Shutter time set to %s us...\n' % exposure_time_to_set)
            
            #TODO maybe print exposure time when automatic
            elif mode=='continuous':
                self._camera.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)
                print('Automatic exposure enabled...')
                
            elif mode=='once':
                self._camera.ExposureAuto.SetValue(PySpin.ExposureAuto_Once)
                print('Automatic exposure enabled...')
            
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False
        return result

    def reset_exposure(self):
        """
        This function returns the camera to a normal state by re-enabling automatic exposure.
    
        :param cam: Camera to reset exposure on.
        :type cam: CameraPtr
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True
    
            if self._camera.ExposureAuto.GetAccessMode() != PySpin.RW:
                print('Unable to enable automatic exposure (node retrieval). Non-fatal error...')
                return False
    
            self._camera.ExposureAuto.SetValue(PySpin.ExposureAuto_Continuous)
        
        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False
    
        return result

    def read(self, image=None):

        cameraImage = self._camera.GetNextImage()
        if cameraImage.IsIncomplete():
            return False, None

        h = cameraImage.GetHeight()
        w = cameraImage.GetWidth()
        numChannels = cameraImage.GetNumChannels()
        if numChannels > 1:
            cameraImageData = cameraImage.GetData().reshape(
                    h, w, numChannels)
        else:
            cameraImageData = cameraImage.GetData().reshape(
                    h, w)

        if image is None:
            image = cameraImageData.copy()
        else:
            image[:] = cameraImageData

        cameraImage.Release()

        return True, image


    def release(self):

        self._camera.EndAcquisition()
        self.reset_exposure()
        self._camera.DeInit()
        
        del self._camera

        self._cameraList.Clear()

        self._system.ReleaseInstance()






import wx
from PIL import Image

SIZE = (1000, 600)
TEST = PySpinCapture(0)
TEST.configure_exposure()
TEST.configure_image_dimensions(width=SIZE[0],height=SIZE[1])
TEST.configure_pixel_format()

def get_image():
    _ , data = TEST.read()
    return Image.fromarray(data, 'L')

def pil_to_wx(image):
    width, height = image.size
    buffer = image.convert('RGB').tobytes()
    bitmap = wx.Bitmap.FromBuffer(width, height, buffer)
    return bitmap

class Panel(wx.Panel):
    def __init__(self, parent):
        super(Panel, self).__init__(parent, -1)
        self.SetSize(SIZE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.update()
    def update(self):
        self.Refresh()
        self.Update()
        wx.CallLater(15, self.update)
    def create_bitmap(self):
        image = get_image()
        bitmap = pil_to_wx(image)
        return bitmap
    def on_paint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(bitmap, 0, 0)

class Frame(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX
        super(Frame, self).__init__(None, -1, 'Camera Viewer', style=style)
        panel = Panel(self)
        self.Fit()

def main():
    app = wx.App()
    frame = Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()
    
if __name__ == '__main__':
    main()
    del TEST
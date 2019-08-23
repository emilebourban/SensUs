#!/usr/bin/env python3

import pygame
import os
import time
from datetime import datetime
import numpy as np
from camera import pyspin_cam as pc
import multiprocessing as mp

import PySpin as spin
#from camera import cam_stream as cs

class Element:

    def __init__(self, screen, color, pos, size, onclick_func, next_layer):
        self.next_layer = next_layer
        self.onclick_func = onclick_func
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size

    def click(self, position):
        x1, y1 = self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2
        x2, y2 = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        if x1 < position[0] < x2 and y1 < position[1] < y2:
            self.onclick_func(self.next_layer)



    def draw(self):
        x1, y1 = self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2
        #x2, y2 = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        pygame.draw.rect(self.screen, self.color, (x1, y1, self.size[0], self.size[1]))


class Message:

    def __init__(self, text, screen, color, pos, size):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size
        self.text = text

    def text_objects(self,font):
        textSurface = font.render(self.text, True, self.color)
        return textSurface, textSurface.get_rect()

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf',self.size)
        TextSurf,TextRect = self.text_objects(font)
        TextRect.center = (self.pos[0], self.pos[1])
        self.screen.blit(TextSurf, TextRect)

    def click(self,position):
        pass

class Image:

    def __init__(self, screen, pos, size, name):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.name = name

    def draw(self):
        img = pygame.image.load(self.name)
        img = pygame.transform.scale(img, (self.size[0], self.size[1]))
        self.screen.blit(img,self.pos)

    def click(self,position):
        pass


class Loading_bar:

    def __init__(self, screen, progression=0):
        self.screen = screen
        self._progression = progression

    @property
    def progression(self):
        return self._progression

    @progression.setter
    def progression(self, v):
        self._progression = max(0, min(1,v))


    def draw(self):
        width = 640 * self.progression
        pygame.draw.rect(self.screen, ( 0, 0, 0), (100, 150, 640, 75), 3)
        pygame.draw.rect(self.screen, ( 0, 0, 0), (100, 150, width, 75))

    def click(self,position):
        pass



class Capture:
    def __init__(self, screen_size):
        self.acquisition_started = False
        self.cam = None
        self.screen_size = screen_size

    def make_cam(self):
        self.cam = pc.Camera()
    
    def plug(self, setting, stream = True):
        self.cam = pc.Camera()
        self.set_acquisition_param(stream)
        self.cam.BeginAcquisition()
        self.acquisition_started = True

        
    def unplug(self):
        if self.acquisition_started:
            self.cam.EndAcquisition()
            self.acquisition_started = False
        self.cam.DeInit()
        self.cam.Clear_cam_list()
        self.cam.Delete()
        self.cam.ReleaseInstance()
        del self.cam
        #TODO maybe add del cam
        
        
    def set_acquisition_param(self, stream):
        if stream:
            self.cam['StreamBufferHandlingMode'].value = 'NewestFirst'
    
            #Setting framerate to maximum
            self.cam['TriggerMode'].value = 'Off'
            self.cam['AcquisitionFrameRateEnable'].value = True
            self.cam['AcquisitionFrameRate'].value = self.cam['AcquisitionFrameRate'].max
            self.cam['StreamCRCCheckEnable'].value = False
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
            
            self.cam['Width'].value = self.screen_size[0]
            self.cam['Height'].value = self.screen_size[1]
        else:
            self.stream = False
            self.cam['StreamBufferHandlingMode'].value = 'NewestOnly'
            #Setting framerate to maximum
            self.cam['TriggerMode'].value = 'Off'
            self.cam['AcquisitionMode'].value = 'Continuous'
                    #TODO give size to constructor depending on window size
            self.cam['Width'].value = self.cam['Width'].max
            self.cam['Height'].value = self.cam['Height'].max
            
            self.cam['StreamCRCCheckEnable'].value = True
    #        self.cam['AcquisitionMode'].value = 'Continuous'
    
            #binning of the image for smaller image size => higher framerate
            self.cam['DecimationSelector'].value = 'All'
            self.cam['BinningHorizontal'].value = 1
            self.cam['BinningVertical'].value = 1
            self.cam['BinningHorizontalMode'].value = 'Average'
            self.cam['BinningVerticalMode'].value = 'Average'
            
            self.cam['GainAuto'].value = 'Off'
            self.cam['ExposureAuto'].value = 'Once'
            #setting pixel format
            self.cam['PixelFormat'].value = 'Mono8'

        #TODO give size to constructor depending on window size
    
    def get_image(self):
        # if you don't want to tie the framerate to the camera, you can check
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.

        #de array a surfacepygame
        if self.stream==True:
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
        else:
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
            
    def BeginAcquisition(self):
        self.cam.BeginAcquisition()
        
    def EndAcquisition(self):
        self.cam.EndAcquisition()
            
    def DeInit(self):
        self.cam.DeInit()
    
    def __del__(self):
        self.unplug()




class Stream(object):

    def __init__(self, screen):
        
        self.screen = screen
        self.size = (self.screen.get_size())
        self.capture = Capture(self.size)
        
    def get_image(self):
        return self.capture.get_image()
    
    def plug(self, stream):
        self.capture.plug(stream)
    
    def unplug(self):
        self.capture.unplug()
    
    def click(self,position):
        pass


    def draw(self):
        snapshot = self.get_image()
        self.screen.blit(snapshot, (0,0))
        
        

class Layer(dict):

    def __init__(self, screen, stream=None):
        self.screen = screen
        self.stream = stream
    def draw_circle(self, center):
        if 100 < center[0] < 700 and 90 < center[1] < 390:
            pygame.draw.circle(self.screen,(255, 0, 0), center, 100) # change the radius according to the scaling
    
    def remove_circle(self):
        for e in self.values():
            if type(e) == list:
                if len(e) > 0:
                    del e[-1]
                else:
                    pass 
            else:
                pass
            
    def draw(self):

        self.screen.fill(( 0, 0, 255))
        for e in self.values():
            if type(e) == list:
                if len(e) > 0:
                    for center in e:
                        self.draw_circle(center)
                else:
                    pass 
            else:
                e.draw()

    def onclick(self,position):
        
        for e in self.values():
            if type(e) == list:
                pass 
            else:
                e.click(position)


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(conn):
    info('function f')
    
    count=0
    inside_loop = True
    while inside_loop and count<30:
        count +=1
#        conn.send(count)
        inside_loop = conn.recv()
        print(conn.recv())

        print('hello')
        time.sleep(0.2)
#        running_img_acqu = conn.recv()
#        conn.send(count)


def acquire_images(capture):     
    try:
        test_file = open('test.txt', 'w+')
    except IOError:
        print('Unable to write to current directory. Please check permissions.')
        input('Press Enter to exit...')
        return False
    test_file.close()
    os.remove(test_file.name)
    capture.plug()
    capture.set_image_acquisition()
    
    save_dir=''

    #Starts iteration to set the gain and exposure time
    for i in range(10):
         # Create a unique filename
        im = capture.get_image()
        print(i)
    num_images = 10
    

    for i in range(num_images):
         # Create a unique filename
        filename = 'Frame_'+'0'*(4 - len(str(i)))+str(i)+'.tif' 
        im = capture.get_image()
        print(datetime.now())
        # Save image
        im.Save(save_dir+filename)
        print('Saved image '+filename)
        time.sleep(2)
    capture.unplug()
        

class Application(dict):

    def __init__(self):
        pygame.init()
        self.active_layer = 'main'
        self.quitting = False
        self.screen = pygame.display.set_mode((800, 480))
        
        def switch_layer_click(new_layer):
            if self.active_layer == 'focus':
                self[self.active_layer]['camera'].unplug()
            elif new_layer == 'focus':
                self[new_layer]['camera'].plug(True)

#                self[new_layer]['camera'] = Capture(self.screen, pc.Camera())
            self.active_layer = new_layer
            

        
        def remove_circle_click(next_layer):
            self[self.active_layer].remove_circle()
        
        def second_onclick_func():
            pass

        
        super().__init__({
        "main": Layer(self.screen),
        "chip": Layer(self.screen),
        "insert": Layer(self.screen),
        "tutorial": Layer(self.screen),
        "focus": Layer(self.screen),
        "loading": Layer(self.screen),
        "circle": Layer(self.screen),
        "results": Layer(self.screen),
        })


        def coordinate_correction(center,pos,size): #pos and size of the image
            scaling_x = 5000/size[0] # adapt when the size is known
            scaling_y = 3000/size[1]
            x_center = pos[0]-size[0]/2
            y_center = pos[1]-size[1]/2
            return ((center[0]-x_center)*scaling_x,(center[1]-y_center)*scaling_y)


    #    def compute_concentration(center):
    #       call the script to compute the compute_concentration
    #       return concentration


#       4 buttons of the first layer
        self['main']['measure'] = Element(self.screen, (255, 255, 255), (420,75), (600,50), switch_layer_click, 'chip')
        self['main']['Profil'] = Element(self.screen, (255, 255, 255), (420,150), (600,50), switch_layer_click,'chip')
        self['main']['Param'] = Element(self.screen, (255, 255, 255), (420,225), (600,50), switch_layer_click,'chip')
        self['main']['Help'] = Element(self.screen, (255, 255, 255), (420,300), (600,50), switch_layer_click,'Katia')
#       4 messages of the first layer
        self['main']['text1']= Message("Measure",self.screen,(0,0,0),(420,75),10)
        self['main']['text2']= Message("Profils",self.screen,(0,0,0),(420,150),10)
        self['main']['text3']= Message("Parameters",self.screen,(0,0,0),(420,225),10)
        self['main']['text4']= Message("Help",self.screen,(0,0,0),(420,300),10)

        #self['main']['image']= Image(self.screen,(0,0),(100,100),'/Users/Clara/Documents/Sensus/gui/test1/gui/1.png')
#       Second Layer
        self['chip']['instruction'] = Element(self.screen, (255, 255, 255), (210,200), (300,50), switch_layer_click,'insert')
        self['chip']['continue'] = Element(self.screen, (255, 255, 255), (630,200), (300,50), switch_layer_click,'insert')
        self['chip']['retour'] = Element(self.screen, (255, 255, 255), (630,300), (300,50), switch_layer_click,'main')

        self['chip']['text1']= Message("Prepare the Chip", self.screen, (0,0,0), (420,50), 30)
        self['chip']['text2']= Message("Instructions", self.screen, (0,0,0), (210,200), 10)
        self['chip']['text3']= Message("Continue", self.screen, (0,0,0), (630,200), 10)
        self['chip']['text4']= Message("Back to menu", self.screen, (0,0,0), (630,300), 10)

        self['insert']['text1']= Message("Insert the Chip", self.screen, (0,0,0), (420,50), 30)
        self['insert']['start'] = Element(self.screen, (255, 255, 255), (420,300), (300,50), switch_layer_click,'focus')
        self['insert']['text2']= Message("Set the focus. When it is done just touch me... ",self.screen,(0,0,0),(420,300),10)

#        self['focus']['camera'] = Stream(self.screen)
        self['focus']['text1'] = Message("Set the focus",self.screen,(0,0,0),(420,50),30)
        self['focus']['start'] = Element(self.screen, (255,255,255), (650,350), (100,50), switch_layer_click, 'loading')
        self['focus']['text2'] = Message('Focus is done', self.screen, (0,0,0), (650,350), 20)
        

        self['tutorial']['text1']= Message("Steps to do the chip", self.screen, (0,0,0), (420,50), 30)
        self['tutorial']['start'] = Element(self.screen, (255, 255, 255), (550,300), (300,50), switch_layer_click,'focus')
        self['tutorial']['text2']= Message("Back to menu", self.screen, (0,0,0), (550,300), 10)

        self['loading']['text1']= Message("Wait a moment", self.screen, (0,0,0), (420,50), 30)
        self['loading']['bar']= Loading_bar(self.screen)

        self['circle']['text1']= Message("Circle detection : ", self.screen, (0,0,0), (420,50), 20)
        self['circle']['start1'] = Element(self.screen, (255, 255, 255), (750,100), (90,50), remove_circle_click, 'circle')
        self['circle']['text2']= Message("Rm", self.screen, (0,0,0), (750,100), 10)
        self['circle']['start2'] = Element(self.screen, (255, 255, 255), (750,300), (90,50), switch_layer_click,'main')
        self['circle']['text3']= Message("Next", self.screen, (0,0,0), (750,300), 10)
        self['circle']['centers'] = []

        self['results']['text1']= Message("Results : ", self.screen, (0,0,0), (420,50), 20)
        


    def run(self):
        try:
            t = time.time()
#            process_started = False
#            parent_conn, child_conn = mp.Pipe()
#            cap = Capture((10,10))
#            p = mp.Process(target=acquire_images, args=(cap,))
#            count = 0
            while not self.quitting:
#                try:
#                    p
#                except NameError:
#                    cap = Capture((10,10))
#                    p = mp.Process(target=acquire_images, args=(cap,))
#                if self.active_layer == 'loading': #TODO: si active layer == 'loading'
#                    if process_started == False:
##                        p = mp.Process(target=acquire_images, args=(self.kamera,))
#                        p.start()
##                        parent_conn.send(True)
##                        print('sent1True')
#                        process_started = True
#                    else:
#                        pass
##                        new_count = parent_conn.recv()
##                        if count == new_count:
##                            pass
##                        else:
##                            parent_conn.send(True)
##                            count = new_count
#                
#                
#                if self.active_layer == 'main': #TODO: si active layer == 'measure aborted'
#                    if p.is_alive():
##                        parent_conn.send(False)
##                        print('sent2False')
##                        time.sleep(5)
##                        parent_conn.close()
##                        child_conn.close()
#                        p.terminate()
#                    del p
#                    process_started = False
##                try:
##                    parent_conn.send(True)
##                except OSError:
#                    print('OS ERROR')
                    
              
#                    p = mp.Process(target=f, args=(Capture(10,10),))

                    
                # animation
                if time.time() - t >= 0.01:
                    if  self.active_layer == 'loading':
                        self['loading']['bar'].progression += 0.001
                        t = time.time()
                        if self['loading']['bar'].progression == 1:
                            self.active_layer = 'circle'
    

#                if self.active_layer =='circle':
#                    p.terminate()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quitting = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.quitting = True
                    if event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            self[self.active_layer].onclick(pos)
                            if self.active_layer == 'circle':
                                self[self.active_layer].draw_circle(pos)
                                self['circle']['centers'].append(pos)
                self[self.active_layer].draw()
                pygame.display.update()
#            self["focus"]['camera'].release()
            pygame.quit()
        except: 
            print('ERROR')
#            del self["focus"]['camera'].kamera
            pygame.quit()
            raise
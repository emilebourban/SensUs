#!/usr/bin/env python3

import pygame
import numpy as np
from time import time
from camera import pyspin_cam as pc
#from camera import cam_stream as cs

class Element:

    def __init__(self, screen, color, pos, size, onclick_func):
        self.onclick_func = onclick_func
        self.screen = screen
        self.color = color
        self.pos = pos
        self.size = size

    def click(self, position):
        x1, y1 = self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2
        x2, y2 = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        if x1 < position[0] < x2 and y1 < position[1] < y2:
            self.onclick_func()



    def draw(self):
        x1, y1 = self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2
        #x2, y2 = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        pygame.draw.rect(self.screen, self.color, (x1, y1, self.size[0], self.size[1]))


class Message:

    def __init__(self, text,screen, color, pos, size):
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


class Layer(dict):

    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.fill(( 0, 0, 255))
        for e in self.values():
            e.draw()

    def onclick(self,position):
        for e in self.values():
            e.click(position)

class Capture(object):
    def __init__(self, click_func):
        
        self.size = (800,480)
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        self.button = Element(self.display,(255,255,255),(650,350),(100,50), click_func)


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
        image.Release()

        self.snapshot = pygame.pixelcopy.make_surface(array)

        # blit it to the display surface.  simple!
        self.display.blit(self.snapshot, (0,0))
        self.button.draw()
        pygame.display.update()
    
    def onclick(self,position):
        for e in self.values():
            e.click(position)
            
    def release(self):         
        self.cam.release()
        
    def __del__(self):
        self.release()
        

    def draw(self):
        pass




class Application(dict):

    def __init__(self):
        pygame.init()
        self.active_layer = 'main'
        self.quitting = False
        self.screen = pygame.display.set_mode((800, 480))
        
        def onclick_func():
            print('onclick')
            self.active_layer = "chip"

        def second_onclick_func():
            pass
    #        self.active_layer = "chip"

        def third_onclick_func():
            self.active_layer = "insert"

        def main_onclick_func():
            self.active_layer = "main"

        def tutorial_onclick_func():
            self.active_layer = "tutorial"

        def start_onclick_func():
            self.active_layer = "loading"

        def focus_onclick_func():
            self.active_layer = "focus"
        
        super().__init__({
        "main": Layer(self.screen),
        "chip": Layer(self.screen),
        "insert": Layer(self.screen),
        "tutorial": Layer(self.screen),
        "focus": Capture(start_onclick_func),
        "loading": Layer(self.screen),
        "results": Layer(self.screen)
        })



#       4 buttons of the first layer
        self['main']['measure'] = Element(self.screen, (255, 255, 255), (420,75), (600,50), onclick_func)
        self['main']['Profil'] = Element(self.screen, (255, 255, 255), (420,150), (600,50), onclick_func)
        self['main']['Param'] = Element(self.screen, (255, 255, 255), (420,225), (600,50), onclick_func)
        self['main']['Help'] = Element(self.screen, (255, 255, 255), (420,300), (600,50), onclick_func)
#       4 messages of the first layer
        self['main']['text1']= Message("Measure",self.screen,(0,0,0),(420,75),10)
        self['main']['text2']= Message("Profils",self.screen,(0,0,0),(420,150),10)
        self['main']['text3']= Message("Parameters",self.screen,(0,0,0),(420,225),10)
        self['main']['text4']= Message("Help",self.screen,(0,0,0),(420,300),10)

        #self['main']['image']= Image(self.screen,(0,0),(100,100),'/Users/Clara/Documents/Sensus/gui/test1/gui/1.png')
#       Second Layer
        self['chip']['instruction'] = Element(self.screen, (255, 255, 255), (210,200), (300,50), tutorial_onclick_func)
        self['chip']['continue'] = Element(self.screen, (255, 255, 255), (630,200), (300,50), third_onclick_func)
        self['chip']['retour'] = Element(self.screen, (255, 255, 255), (630,300), (300,50), main_onclick_func)

        self['chip']['text1']= Message("Prepare the Chip",self.screen,(0,0,0),(420,50),30)
        self['chip']['text2']= Message("Instructions",self.screen,(0,0,0),(210,200),10)
        self['chip']['text3']= Message("Continue",self.screen,(0,0,0),(630,200),10)
        self['chip']['text4']= Message("Back to menu",self.screen,(0,0,0),(630,300),10)

        self['insert']['text1']= Message("Insert the Chip",self.screen,(0,0,0),(420,50),30)
        self['insert']['start'] = Element(self.screen, (255, 255, 255), (420,300), (300,50), focus_onclick_func)
        self['insert']['text2']= Message("Set the focus. When it is done just touch the screen... ",self.screen,(0,0,0),(420,300),10)

    #    self['focus']['text1']= Message("Set the focus",self.screen,(0,0,0),(420,50),30)
    #    self['focus']['start'] = Element(self.screen, (255, 255, 255), (420,300), (300,50), start_onclick_func)
    #    self['focus']['text2']= Message("Start the measure",self.screen,(0,0,0),(420,300),10)


        self['tutorial']['text1']= Message("Steps to do the chip",self.screen,(0,0,0),(420,50),30)
        self['tutorial']['start'] = Element(self.screen, (255, 255, 255), (550,300), (300,50), main_onclick_func)
        self['tutorial']['text2']= Message("Back to menu",self.screen,(0,0,0),(550,300),10)

        self['loading']['text1']= Message("Wait a moment",self.screen,(0,0,0),(420,50),30)
        self['loading']['bar']= Loading_bar(self.screen)

        self['results']['text1']= Message("Results : ",self.screen,(0,0,0),(420,50),20)

    def run(self):
        t = time()
        while not self.quitting:

            # animation
            if time() - t >= 0.01:
                if  self.active_layer == 'loading':
                    self['loading']['bar'].progression += 0.001
                    t = time()
                    if self['loading']['bar'].progression == 1:
                        self.active_layer = 'results'

            if self.active_layer == 'focus':
                self[self.active_layer].get_and_flip()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitting = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quitting = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.active_layer == 'focus':
                        self.active_layer = 'loading'
                    else:
                        pos = pygame.mouse.get_pos()
                        self[self.active_layer].onclick(pos)

            self[self.active_layer].draw()
            pygame.display.update()
        del self["focus"]
        pygame.quit()
        

#!/usr/bin/env python3

from . import gui
from . import layers
from . import acqusition as acq
import pygame
from logging import getLogger
from time import time

# TODO set fullscreen=True at gui.init

class Application(dict):

    def __init__(self, max_fps=30):
        self.log = getLogger('main.app')
        self.screen = gui.init(fullscreen=False)
        super().__init__({
            "main": layers.MainLayer(self),
            "chip": layers.ChipLayer(self),
            "tutorial": layers.TutorialLayer(self),
            "insert": layers.InsertLayer(self),
            "focus": layers.FocusLayer(self),
            "loading": layers.LoadingLayer(self),
            "circle": layers.CircleLayer(self),
            "results": layers.ResultsLayer(self),
        })
        self._active_layer = 'main'
        self.quitting = False
        self.max_fps = max_fps

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, l):
        if l not in self:
            raise KeyError(l)
        self.log.debug(f'Moving to layer "{l}"')
        self._active_layer = l

    def get_image_capture(self):
        self.acq.Capture.get_image(self)

    def get_image_livestream(self):
        self.acq.LiveStream.get_image(self)


    def run(self):
        self.quitting = False
        t = time()
        while not self.quitting:
            # limiting fps
            if time() - t >= 1 / self.max_fps:
                t = time()

                self.exec_events()

                if active_layer == "focus"
                    get_image_livestream()

                if active_layer == "loading"

                    try:
                        test_file = open('test.txt', 'w+')
                    except IOError:
                        print('Unable to write to current directory. Please check permissions.')
                        input('Press Enter to exit...')
                        return False
                    test_file.close()
                    os.remove(test_file.name)
                    save_dir=''
                    num_images = 120

                    for i in range(num_images):

                        filename = 'Frame_'+'0'*(4 - len(str(i)))+str(i)+'.tif'
                        im = get_image_capture()
                        print(datetime.now())
                        # Save image
                        im.Save(save_dir+filename)
                        print('Saved image '+filename)

                self.draw()
        return True


    def exec_events(self):
        for event in pygame.event.get():

            # TODO to remove eventually
            if event.type == pygame.QUIT:
                self.quitting = True

            # TODO to remove eventually
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quitting = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].click_down(pos)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].click_up(pos)

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].mouse_motion(pos)


    def draw(self):
        self[self.active_layer].draw()
        pygame.display.update()

    def __repr__(self):
        layers = {k: v for k, v in self.items()}
        return f'<Application: {layers}>'

    def __del__(self):
        gui.quit()

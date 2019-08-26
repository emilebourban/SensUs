#!/usr/bin/env python3

from . import gui
import os
from . import layers
#from . import image_analysis
from . import ifconfig
from . import photographer
import pygame
from logging import getLogger
from time import time

# TODO set fullscreen=True at gui.init


class Application(dict):

    def __init__(self, is_raspi=True, debug=False, draw_fps=30,
                 ip_refresh_time=1.0, live_fps=24, capture_refresh_time=30):
        self.log = getLogger('main.app')
        self.debug = debug
        self.is_raspi = is_raspi
        self.screen = gui.init(fullscreen=is_raspi, hide_cursor=False)
        self.photographer = photographer.Photographer()
        super().__init__({
            'welcome': layers.WelcomeLayer(self),
            'main': layers.MainLayer(self),
            'chip': layers.ChipLayer(self),
            'tutorial1': layers.Tutorial1Layer(self),
            'tutorial2': layers.Tutorial2Layer(self),
            'tutorial3': layers.Tutorial3Layer(self),
            'tutorial4': layers.Tutorial4Layer(self),
            'tutorial5': layers.Tutorial5Layer(self),
            'insert': layers.InsertLayer(self),
            'focus': layers.FocusLayer(self),
            'loading': layers.LoadingLayer(self),
            'results': layers.ResultsLayer(self),
            'profiles': layers.ProfilesLayer(self),
            'help': layers.HelpLayer(self),
            'parameters': layers.ParametersLayer(self),
        })
        self.over_layer = layers.OverLayer(self)
        self.active_layer = 'welcome'
        self.quitting = False
        self.live_image = None
        self.draw_fps = draw_fps
        self.ip_refresh_time = ip_refresh_time

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, l):
        if l not in self:
            raise KeyError(l)
        self.log.debug(f'Moving to layer "{l}"')
        self._active_layer = l
        if self._active_layer == 'focus':
            self.photographer.set_mode('live_stream')
        if self._active_layer == 'loading':
            self.photographer.set_mode('capture')

    def run(self):
        self.photographer.start()
        self.quitting = False
        t_draw = time()
        t_ip = time()

        while not self.quitting:

            self.log.debug('app run')

            # events
            self.exec_events()

            # get latest photographer's live image
            if not self.photographer.has_new_live_image():
                try:
                    self.live_image = self.photographer.get_new_live_image()
                    self.log.debug(f'Mode set to {self.mode}')
                except BaseException:
                    pass

            # update ip
            if self.debug and time() - t_ip > self.ip_refresh_time:
                t_ip = time()
                self.over_layer['ip'].text = ifconfig.get_ip_addresses_str()

            # drawing
            if time() - t_draw >= 1 / self.draw_fps:
                self.over_layer['fps'].text = 1 / (time() - t_draw)
                t_draw = time()
                self.draw()


        self.photographer.stop()
        self.photographer.join(5)
        return True

    def exec_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quitting = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quitting = True

            # 'd' is pressed -> toggle debug mode
            if event.type == pygame.KEYDOWN and event.key == 100:
                self.debug = not self.debug

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].click_down(pos, False)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].click_up(pos, False)

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self[self.active_layer].mouse_motion(pos, False)

    def draw(self):
        self[self.active_layer].draw()
        if self.debug:
            self.over_layer.draw()
        pygame.display.update()

    def __repr__(self):
        layers = {k: v for k, v in self.items()}
        return f'<Application: {layers}>'

    def __del__(self):
        gui.quit()

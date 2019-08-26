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
        self.screen = gui.init(fullscreen=is_raspi, hide_cursor=is_raspi)
        self.photographer = photographer.Photographer(live_stream_fps=18,
                                                      n_acquisitions=3,
                                                      capture_refresh_time=10)
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
        if self.active_layer == 'main':
            self.photographer.set_mode(None)
        if self.active_layer == 'focus':
            self.photographer.set_mode('live_stream')
        elif self.active_layer == 'loading':
            self.photographer.set_mode('capture')

    def run(self):
        self.log.debug('starting photographer')
        self.photographer.start()
        self.log.debug('photographer started')
        self.quitting = False
        t_draw = time()
        t_ip = time()

        while not self.quitting:

            # events
            self.exec_events()

            # get latest photographer's live image
            if self.photographer.has_new_live_image():
                while self.photographer.has_new_live_image():
                    try:
                        img = self.photographer.get_new_live_image()
                        self.log.debug('Got new live image')
                    except BaseException as e:
                        self.log.warn('Failed to get new live image: {e}')
                img = pygame.pixelcopy.make_surface(img)
                img = pygame.transform.scale(img, (800, 533))
                self.live_image = img

            # update ip
            if self.debug and time() - t_ip > self.ip_refresh_time:
                t_ip = time()
                self.over_layer['ip'].text = ifconfig.get_ip_addresses_str()

            # drawing, update progessbar, update fps, "next" btn
            if time() - t_draw >= 1 / self.draw_fps:
                fps = 1 / (time() - t_draw)
                progress = self.photographer.get_progress()
                self['loading']['progress'].progression = progress
                finished = self.photographer.is_finished()
                self['loading']['next'].disabled = not finished
                self.over_layer['fps'].text = f"{fps:05.2f} fps"
                t_draw = time()
                self.draw()

        self.log.debug('Waiting on photographer to finished...')
        self.photographer.stop()
        self.photographer.join(5)
        if self.photographer.is_alive():
            self.log.debug('Photographer failed to finish')
        else:
            self.log.debug('Photographer finished')
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

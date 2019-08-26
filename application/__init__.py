#!/usr/bin/env python3

from . import gui
import os
import numpy as np
from . import layers
#from . import image_analysis
from . import acquisition
import pygame
from logging import getLogger
from time import time
from subprocess import run, PIPE
import re

# TODO set fullscreen=True at gui.init


class Application(dict):

    def __init__(self, is_raspi=True, debug=False, draw_fps=30,
                 ip_refresh_time=1.0, live_fps=24, capture_refresh_time=30):
        self.log = getLogger('main.app')
        self.debug = debug
        self.is_raspi = is_raspi
        self.screen = gui.init(fullscreen=is_raspi, hide_cursor=False)
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
            'circle': layers.CircleLayer(self),
            'results': layers.ResultsLayer(self),
            'profiles': layers.ProfilesLayer(self),
            'help': layers.HelpLayer(self),
            'parameters': layers.ParametersLayer(self),
        })
        self.over_layer = layers.OverLayer(self)
        self.active_layer = 'welcome'
        self.quitting = False
        self.draw_fps = draw_fps
        self.ip_refresh_time = ip_refresh_time
        self.live_fps = live_fps
        self.capture_refresh_time = capture_refresh_time
        self.acq = None
        self.acq_i = 0
        self.acquisition_mode = None
        self.live_image = None
        self.result_path = 'results/img_'
        self.n_results = 10

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
            self.acquisition_mode = 'live_stream'
        if self._active_layer == 'loading':
            self.acquisition_mode = 'capture'

    @property
    def acquisition_mode(self):
        return self._acquisition_mode

    @acquisition_mode.setter
    def acquisition_mode(self, m):
        if m not in ('capture', 'live_stream', None):
            raise KeyError(m)
        self.log.debug(f'Setting acquisition mode to "{m}"')
        self._acquisition_mode = m

        if m == 'capture':
            del self.acq
            self.acq = acquisition.Capture()
            self.expo_time = self.acq.get_exposure_time()
            self.log.info(f'New expo time: {self.expo_time}us')
            del self.acq
            self.acq = acquisition.LiveStream()
            self.acq_i = 0
        if m is not None:
            del self.acq
            self.acq = acquisition.LiveStream()

    def run(self):
        self.quitting = False
        t_draw = time()
        t_ip = time()
        t_live = time()
        t_capt = time()

        while not self.quitting:

            # livestream
            if self.acquisition_mode and time() - t_live > 1/self.live_fps:
                t_live = time()
                self.live_image = self.acq.get_image()

            # capture
            if self.acquisition_mode == 'capture' \
                    and time() - t_capt > self.capture_refresh_time:
                self.capture()

            # events
            self.exec_events()

            # update ip
            if self.debug and time() - t_ip > self.ip_refresh_time:
                t_ip = time()
                ips = self.get_ip_addresses()
                self.over_layer['ip'].text = ' - '.join(ips)

            # drawing
            if time() - t_draw >= 1 / self.draw_fps:
                t_draw = time()
                self.draw()

        return True

    def capture(self):
        del self.acq
        self.acq = acquisition.Capture(expo_time=self.expo_time)
        img = self.acq.get_image()
        print('>> 1 >> ', img)
        path = self.result_path + f"{self.acq_i:04d}"
        np.save(path, img)
        self.log.debug(f'Capture to "{path}"')
        self.acq_i += 1
        if self.acq_i >= self.n_results:
            self.acquisition_mode = 'live_stream'
        del self.acq
        self.acq = acquisition.LiveStream()
        print('>> 2 >> ', img)

    def get_ip_addresses(self):
        try:
            pat = re.compile('^(\w+):.*$\n\s*inet\s+(\d+\.\d+\.\d+.\d+)',
                             re.MULTILINE)
            cmd = run(['ifconfig'], stdout=PIPE, encoding='utf8').stdout
            return [f"{m.group(1)}: {m.group(2)}" for m in pat.finditer(cmd)]
        except BaseException as e:
            self.log.warn(f'Failed to get ip addresses: {e}')
            return ['Failed to get IP addresses']


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

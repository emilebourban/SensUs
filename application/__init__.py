#!/usr/bin/env python3

from . import gui
from . import layers
import pygame
from logging import getLogger
from time import time
from subprocess import run, PIPE
import re

# TODO set fullscreen=True at gui.init


class Application(dict):

    def __init__(self, debug=False, max_fps=30, ip_refresh_time=1.0):
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
        self.over_layer = layers.OverLayer(self)
        self._active_layer = 'main'
        self.quitting = False
        self.max_fps = max_fps
        self.ip_refresh_time = ip_refresh_time
        self.debug = debug

    @property
    def active_layer(self):
        return self._active_layer

    @active_layer.setter
    def active_layer(self, l):
        if l not in self:
            raise KeyError(l)
        self.log.debug(f'Moving to layer "{l}"')
        self._active_layer = l

    def run(self):
        self.quitting = False
        t = time()
        t_ip = time()
        while not self.quitting:
            # update ip
            if self.debug and time() - t_ip > self.ip_refresh_time:
                t_ip = time()
                ips = self.get_ip_addresses()
                self.over_layer['ip'].text = ' - '.join(ips)
            # limiting fps
            if time() - t >= 1 / self.max_fps:
                t = time()
                self.exec_events()
                self.draw()
        return True

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

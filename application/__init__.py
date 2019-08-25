#!/usr/bin/env python3

from . import gui
from . import layers
import pygame
from logging import getLogger
from time import time

# TODO set fullscreen=True at gui.init

class Application(dict):

    def __init__(self, max_fps=30):
        self.log = getLogger('hello.app')
        self.screen = gui.init(fullscreen=False)
        super().__init__({
            "hello": layers.Hello(self),
            "main": layers.MainLayer(self),
            "chip": layers.ChipLayer(self),
            "tutorial1": layers.TutorialLayer1(self),
            "tutorial2": layers.TutorialLayer2(self),
            "tutorial3": layers.TutorialLayer3(self),
            "tutorial4": layers.TutorialLayer4(self),
            "tutorial5": layers.TutorialLayer5(self),
            "insert": layers.InsertLayer(self),
            "focus": layers.FocusLayer(self),
            "loading": layers.LoadingLayer(self),
            "circle": layers.CircleLayer(self),
            "results": layers.ResultsLayer(self),
        })
        self._active_layer = 'hello'
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

    def run(self):
        self.quitting = False
        t = time()
        while not self.quitting:
            # limiting fps
            if time() - t >= 1 / self.max_fps:
                t = time()
                self.exec_events()
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

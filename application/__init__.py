#!/usr/bin/env python3

from . import gui
from . import layers
from . import acquisition as acq
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

    def get_image_capture(self):
        self.acq.Capture.get_image(self)

    def get_image_livestream(self):
        self.acq.LiveStream.get_image(self)


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

                if self.active_layer == "focus":
                    self.get_image_livestream()

                if self.active_layer == "loading":

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

from threading import Thread, Event
from queue import Queue, Full, Empty
from time import time
from logging import getLogger
from . import acquisition
import numpy as np


class Photographer(Thread):

    # !! FROM THE OUTSIDE, ONLY CALL start(), set_mode(...),
    # !! has_new_live_image(), get_new_live_image() and stop()

    def __init__(self, capture_path='results/img_', n_acquisitions=10,
                 live_stream_fps=24, capture_refresh_time=30):
        Thread.__init__(self)
        self.log = getLogger('main.Photographer')
        self.log.debug('Photographer created')
        self.mode_queue = Queue()
        self.live_image_queue = Queue(8)
        self.live_stream_fps = live_stream_fps
        self.capture_refresh_time = capture_refresh_time
        self.capture_path = capture_path
        self.n_acquisitions = 10
        self.acquisition = None
        self.acquisition_i = 0
        self.mode = None
        self.quitting = Event()

    def set_mode(self, m):
        if m not in (None, 'live_stream', 'capture'):
            raise KeyError(m)
        self.mode_queue.put(m)

    def has_new_live_image(self):
        return not self.live_image_queue.empty()

    def get_new_live_image(self):
        return self.live_image_queue.get()

    def run(self):
        self.log.debug('Photographer start')
        t_live = time()
        t_capt = time()

        while not self.quitting.is_set():

            # get new mode
            if not self.mode_queue.empty():
                try:
                    self._set_mode(self.mode_queue.get(block=False))
                    self.log.debug(f'Mode set to {self.mode}')
                except Empty:
                    pass

            # capture
            if self.mode == 'capture' \
                    and time() - t_capt > self.capture_refresh_time:
                t_capt = time()
                self.log.debug('Photographe capture')
                self.capture()

            # livestream
            if self.mode \
                    and time() - t_live > 1 / self.live_stream_fps:
                t_live = time()
                self.log.debug('Photographe live_stream')
                live_image = self.acquisition.get_image()
                try:
                    self.live_image.put(live_image)
                except Full:
                    self.log.warn('Live stream frame drop, (queue is full)')

    def stop(self):
        self.log.debug('stop signal')
        self.quitting.set()

    def capture(self):
        del self.acquisition
        self.acquisition = acquisition.Capture(expo_time=self.expo_time)
        img = self.acquisition.get_image()
        path = self.result_path + f"{self.acquisition_i:04d}"
        np.save(path, img)
        self.log.debug(f'Capture to "{path}"')
        self.acquisition_i += 1
        if self.acquisition_i >= self.n_acquisitions:
            self.log.info('Capture mode ended')
            self.acquisition_mode = 'live_stream'
        del self.acquisition
        self.acquisition = acquisition.LiveStream()

    def _set_mode(self, m):
        if m not in ('capture', 'live_stream', None):
            raise KeyError(m)
        self.log.debug(f'Setting acquisition mode to "{m}"')
        self.mode = m

        if m == 'capture':
            del self.acquisition
            self.acquisition = acquisition.Capture()
            self.expo_time = self.acquisition.get_exposure_time()
            self.log.info(f'New expo time: {self.expo_time}us')
            del self.acquisition
            self.acquisition = acquisition.LiveStream()
            self.acquisition_i = 0

        if m == 'live_stream':
            del self.acquisition
            self.acquisition = acquisition.LiveStream()

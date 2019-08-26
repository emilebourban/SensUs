from threading import Thread, Event, Lock
from queue import Queue, Full, Empty
from time import time
from logging import getLogger
from . import acquisition
import numpy as np


class Photographer(Thread):

    # !! FROM THE OUTSIDE, ONLY CALL start(), set_mode(...),
    # !! has_new_live_image(), get_new_live_image(), get_progess() and stop()

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
        self._start_time = None
        self._start_time_lock = Lock()

    @property
    def start_time(self):
        with self._start_time_lock:
            return self._start_time

    @start_time.setter
    def start_time(self, t):
        with self._start_time_lock:
            self._start_time = t

    def get_progress(self):
        start_time = self.start_time
        total_time = self.n_acquisitions * self.capture_refresh_time
        if start_time is None:
            return 0
        v = max(min((time() - start_time) / total_time, 1), 0)
        return v

    def set_mode(self, m):
        if m not in (None, 'live_stream', 'capture'):
            raise KeyError(m)
        self.log.debug(f'Putting mode: {m}')
        self.mode_queue.put(m)
        self.log.debug(f'Put mode: {m}')

    def has_new_live_image(self):
        return self.live_image_queue.empty() is not True

    def get_new_live_image(self):
        return self.live_image_queue.get(False)

    def run(self):
        self.log.debug('Photographer start')
        t_live = time()
        t_capt = time()

        while not self.quitting.is_set():

            # get new mode
            if not self.mode_queue.empty():
                try:
                    while not self.mode_queue.empty():
                        mode = self.mode_queue.get(block=False)
                    self._set_mode(mode)
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
                self.live_stream()

    def stop(self):
        self.log.debug('stop signal')
        self.quitting.set()

    def capture(self):
        try:
            del self.acquisition
            self.acquisition = acquisition.Capture(expo_time=self.expo_time)
            img = self.acquisition.get_image()
            self.log.debug(f'>>> capture res: {img.shape}')
            path = self.capture_path + f"{self.acquisition_i:04d}"
            np.save(path, img)
            self.log.debug(f'Capture to "{path}"')
            self.acquisition_i += 1
            if self.acquisition_i >= self.n_acquisitions:
                self.log.info('Capture mode ended')
                self.acquisition_mode = 'live_stream'
            del self.acquisition
            self.acquisition = acquisition.LiveStream()
        except BaseException as e:
            self.log.exception(f'Capture acquisition failed {e}')

    def live_stream(self):
        try:
            live_image = self.acquisition.get_image()
            try:
                self.live_image_queue.put(live_image, False)
            except Full:
                self.log.warn('Live stream frame drop, (queue is full)')
        except BaseException as e:
            self.log.exception(f'Live stream acquisition failed {e}')

    def _set_mode(self, m):
        try:
            if m not in ('capture', 'live_stream', None):
                raise KeyError(m)
            self.log.debug(f'Setting acquisition mode to "{m}"')
            self.mode = m

            if m == 'capture':
                self.start_capture_mode()
            if m == 'live_stream':
                self.start_live_stream_mode()

        except BaseException as e:
            self.log.exception(f'Failed to set mode to {m}: {e}')

    def start_capture_mode(self):
        del self.acquisition
        self.acquisition_i = 0
        self.start_time = time()
        self.acquisition = acquisition.Capture()
        self.expo_time = self.acquisition.get_exposure_time()
        self.log.info(f'New expo time: {self.expo_time}us')
        del self.acquisition
        self.acquisition = acquisition.LiveStream()

    def start_live_stream_mode(self):
        del self.acquisition
        self.acquisition = acquisition.LiveStream()

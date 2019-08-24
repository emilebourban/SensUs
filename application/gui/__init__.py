import pygame
from .base import Element, Clickable, RectangleClickable
from logging import getLogger
from weakref import ref
from subprocess import run, PIPE
from collections import OrderedDict
import re

# TODO dragaeble circles


def get_screen_resolution(log):
    try:
        xrandr = run(['xrandr'], stdout=PIPE, encoding='utf8').stdout
        res = re.search('\s*(\d+x\d+).*\*', xrandr).group(1).split('x')
        res = [int(i) for i in res]
    except BaseException as e:
        log.exception('Failed to get screen resolution: {e}')
    log.info(f'Screen resolution: {res[0]}x{res[1]}')
    return res


def init(fullscreen=True):
    log = getLogger('main.gui')
    pygame.init()
    log.debug('Pygame initialized')
    res = get_screen_resolution(log)
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if fullscreen:
        return pygame.display.set_mode(res, flags | pygame.FULLSCREEN)
    return pygame.display.set_mode((800, 400), flags)


def quit():
    pygame.quit()


class Layer(OrderedDict):

    def __init__(self, app, bg_color=(200, 200, 255)):
        self.app = ref(app)
        self.bg_color = bg_color
        self.log = getLogger('main.layer')

    @property
    def screen(self):
        return self.app().screen

    @property
    def clickable_elements(self):
        def is_clickable(e):
            return isinstance(e, Clickable)

        return OrderedDict([(k, v) for k, v in self.items() if is_clickable(v)])

    def draw(self):
        self.screen.fill(self.bg_color)
        for element in self.values():
            try:
                element.draw()
            except BaseException as e:
                self.log.exception(f'Failed to draw element: {e}')

    def click_down(self, pos):
        for e in reversed(self.clickable_elements.values()):
            try:
                e.click_down(pos)
            except BaseException as e:
                self.log.exception(f'Failed to exec click down: {e}')

    def click_up(self, pos):
        for e in reversed(self.clickable_elements.values()):
            try:
                e.click_up(pos)
            except BaseException as e:
                self.log.exception(f'Failed to exec click up: {e}')


class Text(Element):

    # TODO tune default font_size
    def __init__(self, layer, pos, text, font_size=18, color=(0, 0, 0),
                 font='fonts/texgyreheros-regular.otf'):
        super().__init__(layer, pos)
        self.fg_color = color
        self.font_size = font_size
        self.text = text
        self.font = pygame.font.Font(font, self.font_size)

    def text_objects(self):
        surf = self.font.render(self.text, True, self.fg_color)
        return surf, surf.get_rect()

    def draw(self):
        surf, rect = self.text_objects()
        rect.center = self.pos
        # TODO center text ?
        self.screen.blit(surf, rect)


class Image(Element):

    def __init__(self, layer, pos, path, w=None, h=None):
        super().__init__(layer, pos)
        self.img = pygame.image.load(self.path)
        iw, ih = self.img.get_width(), self.img.get_height()
        r = iw / ih
        if not w and not h:
            w, h = iw, ih
        elif not w:
            w, h = ih * r, ih
        else:
            w, h = iw, iw / r
        # TODO check not mixed up w and h
        self.img = pygame.transform.scale(self.img, w, h)

    def draw(self):
        self.screen.blit(self.img, self.pos)


class Rectangle(Element):

    def __init__(self, layer, pos, size, color=(255, 0, 0)):
        super().__init__(self, layer, pos)
        self.size = size
        self.bg_color = color

    def draw(self, force_color=None):
        c, s = self.pos, self.size
        x, y = c[0] - s[0] / 2, c[1] - s[1] / 2
        color = force_color if force_color else self.bg_color
        pygame.draw.rect(self.screen, color, [x, y, *s])


class Button(Rectangle, Text, RectangleClickable):

    def __init__(self, layer, pos, size, text, action):
        Rectangle.__init__(self, layer, pos, size, (255, 220, 200))
        Text.__init__(self, layer, pos, text)
        RectangleClickable.__init__(self, pos, size)
        self.action = action
        self.is_pressed = False

    def draw(self):
        if self.is_pressed:
            Rectangle.draw(self, (100, 255, 0))
        else:
            Rectangle.draw(self)
        Text.draw(self)

    def on_click_down(self, inside):
        if inside:
            self.is_pressed = True
            return True
        return True

    def on_click_up(self, inside):
        self.is_pressed = False
        if inside:
            self.action()
            return True
        return False


class Loading_bar(Element):

    # TODO tune padding default value
    # TODO set colors
    def __init__(self, layer, pos, size, bg_color=(255, 0, 0),
                 fg_color=(0, 0, 255), padding=1, progress=0):
        super().__init__(layer, pos)
        self._progress = progress
        self.size = size

    @property
    def progression(self):
        return self._progress

    @progression.setter
    def progression(self, v):
        self._progress = max(0, min(1, v))

    def draw(self):
        c, s, p, v = self.pos, self.size, self.padding, self.progression
        x1, y1 = c[0] - s[0]/2, c[1] - s[1]/2
        x2, y2 = c[0] + s[0]/2, c[1] + s[1]/2
        px1, py1 = x1 + p, y1 + p
        px2, py2 = px1 + v * (s[0] - 2 * p), y2 - p
        # TODO check remove last arg: 3
        pygame.draw.rect(self.screen, self.bg_color, (x1, y1, x2, y2), 3)
        pygame.draw.rect(self.screen, self.fg_color, (px1, py1, px2, py2))

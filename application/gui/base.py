from weakref import ref


class Element:

    def __init__(self, layer, pos):
        self._layer = ref(layer)
        self.pos = pos

    @property
    def layer(self):
        return self._layer()

    @property
    def screen(self):
        return self.layer.screen

    def draw(self):
        raise NotImplementedError()


class Clickable:

    def click_down(self, pos):
        return self.on_click_down(self.is_in(pos))

    def click_up(self, pos):
        return self.on_click_up(self.is_in(pos))

    def is_in(self, pos):
        return False

    def on_click_down(self):
        pass

    def on_click_up(self):
        pass


class RectangleClickable(Clickable):

    def __init__(self, center, size):
        c, s = center, size
        self.x1 = c[0] - s[0]/2
        self.y1 = c[1] - s[1]/2
        self.x2 = c[0] + s[0]/2
        self.y2 = c[1] + s[1]/2

    def is_in(self, pos):
        if self.x1 <= pos[0] <= self.x2 and self.y1 <= pos[1] <= self.y2:
            return True


class CircleClickable(Clickable):

    def __init__(self, center, radius):
        self.c = center
        self.r = radius

    def is_in(self, pos):
        # TODO: circle enough large ?
        if pos[0] <= self.r and pos[1] <= self.r:
            return True

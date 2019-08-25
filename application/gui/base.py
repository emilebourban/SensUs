from weakref import ref


class Element:

    def __init__(self, layer, pos):
        self._layer = ref(layer)
        self.pos = pos

    @property
    def layer(self):
        return self._layer()

    def app(self):
        return self._layer_app()

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

    def on_click_down(self, inside):
        pass

    def on_click_up(self, inside):
        pass


class MouseMotionSensitive:

    def mouse_motion(self, pos):
        pass


class Draggable(Element, MouseMotionSensitive):
    def __init__(self, layer, pos):
        Element.__init__(self, layer, pos)
        self.dragging = False

    def drag_start(self):
        self.dragging = True

    def drag_stop(self):
        self.dragging = False

    def mouse_motion(self, pos):
        if self.dragging:
            self.pos = pos

    def on_click_down(self, inside):
        if inside:
            self.draw_start()

    def on_click_up(self, inside):
        self.draw_stop()


class RectangleClickable(Clickable):

    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def is_in(self, pos):
        c, s = self.pos, self.size
        x1 = c[0] - s[0]/2
        y1 = c[1] - s[1]/2
        x2 = c[0] + s[0]/2
        y2 = c[1] + s[1]/2
        if x1 <= pos[0] <= x2 and y1 <= pos[1] <= y2:
            return True
        return False


class CircleClickable(Clickable):

    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius

    def is_in(self, pos):
        dx, dy = pos[0] - self.pos[0], pos[1] - self.pos[1]
        r2 = dx**2 + dy**2
        # TODO: circle enough large ?
        if r2 <= self.radius**2:
            return True
        return False

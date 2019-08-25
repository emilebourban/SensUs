from . import gui
from itertools import count


class Layer(gui.Layer):

    def __init__(self, app):
        gui.Layer.__init__(self, app)

    def set_layer(self, l):
        self.app.active_layer = l


class OverLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['ip'] = gui.Text(self, (400, 16), '-', font_size=11)

    # overwrite draw to avoid drawing the background
    def draw(self):
        gui.Group.draw(self)


class MainLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['measure'] = gui.Button(self, (420, 75), size,
                                     'Measure',
                                     lambda: self.set_layer('chip'))
        self['profil'] = gui.Button(self, (420, 150), size,
                                    'Profils',
                                    lambda: self.set_layer('chip'))
        self['param'] = gui.Button(self, (420, 225), size,
                                   'Parameters',
                                   lambda: self.set_layer('chip'))
        self['help'] = gui.Button(self, (420, 300), size,
                                  'Help',
                                  lambda: self.set_layer('circle'))

        # TODO remove this element
        self['circle'] = gui.DetectionCircle(self, (100, 100), 32)
        {1, 2, 34}


class ChipLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['set'] = gui.Text(self, (420, 75),
                               'Prepare the chip')
        self['instruction'] = gui.Button(self, (420, 150), size,
                                         'Instructions',
                                         lambda: self.set_layer('tutorial'))
        self['continue'] = gui.Button(self, (420, 225), size,
                                      'Skip instructions',
                                      lambda: self.set_layer('insert'))
        self['back'] = gui.Button(self, (420, 300), size,
                                  'Back to menu',
                                  lambda: self.set_layer('main'))


class TutorialLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['instruction'] = gui.Text(self, (420, 75),
                                       'Follow the instructions')
        self['continue'] = gui.Button(self, (420, 225), size,
                                      'Continue',
                                      lambda: self.set_layer('insert'))
        self['back'] = gui.Button(self, (420, 150), size,
                                  'Back to menu',
                                  lambda: self.set_layer('insert'))


class InsertLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        self['insert'] = gui.Text(self, (420, 75),
                                  'Insert the chip')
        self['continue'] = gui.Button(self, (420, 225), size,
                                      'Continue',
                                      lambda: self.set_layer('focus'))

class FocusLayer(Layer):
    # TODO: add a stream object in initGui
    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['set'] = gui.Text(self, (420, 75),
                               'Set the focus')
        self['stream'] = gui.Video(self(0,0))
        self['finised'] = gui.Button(self, (420, 150), size,
                                     'Focus is done',
                                     lambda: self.set_layer('loading'))


class LoadingLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['wait'] = gui.Text(self, (420, 75),
                                'Wait a moment')
        self['bar'] = gui.Loading_bar(self, (420, 225), size,
                                      lambda: self.set_layer('circle'))


class CircleLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['wait'] = gui.Text(self, (420, 75),
                                'Choose the cercle')
        self['circles'] = gui.Group()
        self['add'] = gui.Button(self, (600, 50), (40, 40), '+',
                                 lambda: self.new_circle((100, 100), 42))
        self['rem'] = gui.Button(self, (660, 50), (40, 40), '-',
                                 lambda: self.rem_selected_circles())

    def get_new_key(self):
        for i in count():
            if i not in self['circles']:
                return i

    def get_selected_circles(self):
        return {k for k, v in self['circles'].items() if v.is_selected}

    def set_circles(self, circles):
        circles = [gui.DetectionCircle(self, p, r) for p, r in circles]
        circles = [(self.get_new_key(), c) for c in circles]
        self['circles'] = gui.Group(circles)

    def new_circle(self, p, r):
        circle = gui.DetectionCircle(self, p, r)
        self['circles'][self.get_new_key()] = circle

    def rem_selected_circles(self):
        for k in self.get_selected_circles():
            del self['circles'][k]


class ResultsLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['result'] = gui.Text(self, (420, 75),
                                  'The result')
        self['back'] = gui.Button(self, (420, 150), size,
                                  'Back to menu',
                                  lambda: self.set_layer('main'))

'''
class MainLayer(Layer):

    def __init__(self, app):
        Layer.__init__(self, app)
        size = (200, 40)
        p = (200, 200)
        self['measure'] = gui.Button(self, (200, 100), size, 'Measure',
                                     lambda: self.self.set_layer('chip'))
        self['profile'] = gui.Button(self, (200, 200), size, 'Profiles',
                                     lambda: self.self.set_layer('chip'))
'''

from . import gui


class Layer(gui.Layer, dict):

    def __init__(self, app):
        gui.Layer.__init__(self, app)
        dict.__init__(self)

    def set_layer(self, l):
        self.app().active_layer = l


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


class FocusLayer(Layer):
    # TODO: add a stream object in initGui
    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['set'] = gui.Text(self, (420, 75),
                               'Set the focus')
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
        self['add'] = gui.Button(self, (600, 50), (40, 40), '+',
                                 lambda: self.new_circle((100, 100), 42))

    def get_circles_keys(self):
        n = len(self.circle_prefix)
        return {k for k in self.keys() if k[:n] == self.circle_prefix}

    def set_circles(self, circles):
        for k in self.get_circles_keys():
            del self[k]
        for i, c in enumerate(circles):
            circle = gui.DetectionCircle(self, *c)
            self[self.circle_prefix + str(i)] = circle

    def new_circle(self, p, r):
        n = len(self.get_circles_keys())
        circle = gui.DetectionCircle(self, p, r)
        self[self.circle_prefix + str(n)] = circle


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

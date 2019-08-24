from . import gui


class Layer(gui.Layer, dict):

    def __init__(self, app):
        gui.Layer.__init__(self, app)
        dict.__init__(self)

    def set_layer(self, l):
        self.app().active_layer = l


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
                                  lambda: self.set_layer('chip'))

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
        self['bar'] = gui.Loading_bar(self.screen, (420, 225), size,
                                      lambda: self.set_layer('circle'))


class CircleLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['wait'] = gui.Text(self, (420, 75),
                                'Choose the cercle')
        self['circle'] = gui.Button(self.screen, (420, 150), size,
                                    'Detection done',
                                    lambda: self.set_layer('results'))


class ResultsLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['result'] = gui.Text(self.screen, (420, 75),
                                  'The result')
        self['back'] = gui.Button(self.screen, (420, 150), size,
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

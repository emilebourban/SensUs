from . import gui


class Layer(gui.Layer, dict):

    def __init__(self, app):
        gui.Layer.__init__(self, app)
        dict.__init__(self)

    def set_layer(self, l):
        self.app().active_layer = l

class Hello(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (800, 150)
        self['logo'] = gui.Image(self,[250,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/logo_final.png',W =2, H=2)
        self['Hello'] = gui.Button(self, (400, 350), size,
                            'Swiss Precision for Healthcare Improvement',
                            lambda: self.set_layer('main'), fontsize=25, color=(218,41,28))


class MainLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (300, 50)
        self['land'] = gui.Image(self,[0,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/landscape.png',W =1, H=1)
        self['para'] = gui.Image(self,[190,200],'/Users/KatiaSchalk/Desktop/SensUs/Images/param.png',W =2, H=2)
        self['measu'] = gui.Image(self,[190,50],'/Users/KatiaSchalk/Desktop/SensUs/Images/measure.png',W =2, H=2)
        self['prof'] = gui.Image(self,[190,125],'/Users/KatiaSchalk/Desktop/SensUs/Images/profil.png',W =2, H=2)
        self['hel'] = gui.Image(self,[190,275],'/Users/KatiaSchalk/Desktop/SensUs/Images/help.png',W =2, H=2)

        self['Start Analysis'] = gui.Button(self, (400, 75), size,
                                     'Start Analysis',
                                     lambda: self.set_layer('chip'))
        self['Profils'] = gui.Button(self, (400, 150), size,
                                    'Profils',
                                    lambda: self.set_layer('chip'))
        self['param'] = gui.Button(self, (400, 225), size,
                                   'Parameters',
                                   lambda: self.set_layer('chip'))
        self['help'] = gui.Button(self, (400, 300), size,
                                  'Help',
                                  lambda: self.set_layer('chip'))



        # TODO remove this element
        #self['circle'] = gui.DetectionCircle(self, (100, 100), 32)
        #{1, 2, 34}


class ChipLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (300, 50)
        size_bis =(60,33)

        self['land'] = gui.Image(self,[0,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/landscape.png',W =1, H=1)
        self['continu'] = gui.Image(self,[210,125],'/Users/KatiaSchalk/Desktop/SensUs/Images/continue.png',W =2, H=2)
        self['questions'] = gui.Image(self,[210,200],'/Users/KatiaSchalk/Desktop/SensUs/Images/questions.png',W =2, H=2)
        self['home'] = gui.Image(self,[10,13],'/Users/KatiaSchalk/Desktop/SensUs/Images/Home.png',W =3, H=3)

        self['set'] = gui.Text(self, (420, 50),
                               'Prepare the chip', font_size=35)
        self['instruction'] = gui.Button(self, (420, 225), size,
                                         'Instructions',
                                         lambda: self.set_layer('tutorial1'))
        self['continue'] = gui.Button(self, (420, 150), size,
                                      'Skip instructions',
                                      lambda: self.set_layer('insert'))
        self['back'] = gui.Button(self, (70, 30), size_bis,
                                  'Home',
                                  lambda: self.set_layer('main'))





class TutorialLayer1(Layer):

    def __init__(self, app,bg_color=(28, 25, 255)):
        super().__init__(app)
        size = (100, 40)
        size_bis =(120,40)

        self['continue'] = gui.Button(self, (700, 375), size,
                                      'Next',
                                      lambda: self.set_layer('tutorial2'), couleur=(220,220,220))
        self['back'] = gui.Button(self, (100, 375), size_bis,
                                  'Back to menu',
                                  lambda: self.set_layer('chip'), couleur=(220,220,220))

        self['tuto1'] = gui.Image(self,[80,20],'/Users/KatiaSchalk/Desktop/SensUs/Images/tuto1.png',W =3, H=3)



class TutorialLayer2(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (100, 40)

        self['continue'] = gui.Button(self, (700, 375), size,
                                    'Next',
                                    lambda: self.set_layer('tutorial3'), couleur=(220,220,220))
        self['back'] = gui.Button(self, (100, 375), size,
                                'Previous',
                                lambda: self.set_layer('tutorial1'), couleur=(220,220,220))

        self['tuto2'] = gui.Image(self,[100,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/tuto2.png',W =3, H=3)

class TutorialLayer3(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (100, 40)

        self['continue'] = gui.Button(self, (700, 375), size,
                                    'Next',
                                    lambda: self.set_layer('tutorial4'), couleur=(220,220,220))
        self['back'] = gui.Button(self, (100, 375), size,
                                'Previous',
                                lambda: self.set_layer('tutorial2'), couleur=(220,220,220))

        self['tuto3'] = gui.Image(self,[100,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/tuto3.png',W =3, H=3)

class TutorialLayer4(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (100, 40)


        self['continue'] = gui.Button(self, (700, 375), size,
                                    'Next',
                                    lambda: self.set_layer('tutorial5'), couleur=(220,220,220))
        self['back'] = gui.Button(self, (100, 375), size,
                                    'Previous',
                                    lambda: self.set_layer('tutorial3'), couleur=(220,220,220))
        self['tuto4'] = gui.Image(self,[100,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/tuto4.png',W =3, H=3)

class TutorialLayer5(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (100, 40)

        self['continue'] = gui.Button(self, (700, 375), size,
                                    'Next',
                                    lambda: self.set_layer('insert'), couleur=(220,220,220))
        self['back'] = gui.Button(self, (100, 375), size,
                                'Previous',
                                lambda: self.set_layer('tutorial4'), couleur=(220,220,220))

        self['tuto5'] = gui.Image(self,[60,0],'/Users/KatiaSchalk/Desktop/SensUs/Images/tuto5.png',W =3, H=3)

class InsertLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (100, 40)
        size_bis =(120,40)

        self['insert'] = gui.Text(self, (420, 50),
                                  'Insert the chip', font_size=35)
        self['continue'] = gui.Button(self, (700, 375), size,
                                    'Next',
                                    lambda: self.set_layer('focus'), couleur=(220,220,220))

        self['back'] = gui.Button(self, (100, 375), size_bis,
                                  'Back to menu',
                                  lambda: self.set_layer('chip'), couleur=(220,220,220))


        self['device'] = gui.Image(self,[300,100],'/Users/KatiaSchalk/Desktop/SensUs/Images/device.png',W =18, H=18)

        self['chip'] = gui.Image(self,[500,200],'/Users/KatiaSchalk/Desktop/SensUs/Images/chip.png',W =5, H=5)


class FocusLayer(Layer):
    # TODO: add a stream object in initGui
    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['set'] = gui.Text(self, (420, 50),
                               'Set the focus', font_size=35)
        self['finised'] = gui.Button(self, (420, 150), size,
                                     'Focus is done',
                                     lambda: self.set_layer('loading'))


class LoadingLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)
        self['wait'] = gui.Text(self, (420, 50),
                                'Wait a moment', font_size=35)
        self['bar'] = gui.Loading_bar(self.screen, (420, 225), size,
                                      lambda: self.set_layer('circle'))


class CircleLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['wait'] = gui.Text(self, (420, 50),
                                'Choose the cercle', font_size=35)
        self['circle'] = gui.Button(self.screen, (420, 150), size,
                                    'Detection done',
                                    lambda: self.set_layer('results'))


class ResultsLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        size = (200, 40)

        self['result'] = gui.Text(self.screen, (420, 50),
                                  'The result', font_size=35)
        self['back'] = gui.Button(self.screen, (700, 350), size,
                                  'Back to menu',
                                  lambda: self.set_layer('hello'))

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

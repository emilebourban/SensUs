from . import gui
from itertools import count


class Layer(gui.Layer):

    background = None

    def __init__(self, app):
        gui.Layer.__init__(self, app)
        if self.background is None:
            self.background = gui.Image(self, [800/2, 480/2],
                                        'images/background.jpg',
                                        h=480)

    def set_layer(self, l):
        self.app.active_layer = l

    def create_background(self):
        self['bg'] = self.background

    def create_buttons_list(self, buttons):
        w_btn = 300
        h_btn = 50
        pitch = 75
        x_img = 220
        x_btn = 420
        y0 = round(480/2 - len(buttons)/2 * pitch)
        for n, (k, title, path, action) in enumerate(buttons):
            y = y0 + n * pitch
            self['img_' + k] = gui.Image(self, [x_img, y], path, h=h_btn)
            self[k] = gui.Button(self, [x_btn, y], [w_btn, h_btn], title,
                                 action)

    def create_small_buttons_list(self, buttons):
        w_btn = 300
        h_btn = 32
        pitch = 40
        x_btn = 400
        y0 = round(480/2 - len(buttons)/2 * pitch)
        for n, (k, title, action) in enumerate(buttons):
            y = y0 + n * pitch
            self[k] = gui.Button(self, [x_btn, y], [w_btn, h_btn], title,
                                 action)

    def create_next_button(self, target, text='Next', size=[150, 40],
                           disabled=False):
        pos = (800 - 100, 480 - 120)
        self['next'] = gui.Button(self, pos, size, text,
                                  lambda: self.set_layer(target),
                                  disabled=disabled)

    def create_back_button(self, target, text='Back', size=[150, 40]):
        pos = (0 + 100, 480 - 120)
        self['back'] = gui.Button(self, pos, size, text,
                                  lambda: self.set_layer(target))

    def create_title(self, title):
        self['title'] = gui.Text(self, (400, 50), title, font_size=35)


class OverLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['ip'] = gui.Text(self, (400, 16), '-', font_size=11)

    # overwrite draw to avoid drawing the background
    def draw(self):
        gui.Group.draw(self)


class WelcomeLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self['logo'] = gui.Image(self, (400, 160),
                                 'images/logo.png',
                                 h=300)
        self['text'] = gui.Text(self, (400, 350),
                                'Swiss Precision for Healthcare Improvement',
                                font_size=25, color=(218, 41, 28))

    def click_down(self, pos, catched):
        self.app.active_layer = 'main'
        return True


class MainLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        btn_list = [
            ('measure', 'Start analysis', 'images/measure.png',
             lambda: self.set_layer('chip')),
            ('profiles', 'Profiles', 'images/profile.png',
             lambda: self.set_layer('profiles')),
            ('param', 'Parameters', 'images/param.png',
             lambda: self.set_layer('parameters')),
            ('help', 'Help', 'images/help.png',
             lambda: self.set_layer('help')),
        ]
        self.create_background()
        self.create_buttons_list(btn_list)
        self.create_back_button('welcome', 'Suspend')


class ChipLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        btn_list = [
            ('instructions', 'Instructions', 'images/questions.png',
             lambda: self.set_layer('tutorial1')),
            ('skip', 'Skip instructions', 'images/continue.png',
             lambda: self.set_layer('insert')),
        ]
        self.create_background()
        self.create_title('Prepare the chip')
        self.create_buttons_list(btn_list)
        self.create_back_button('main')


class Tutorial1Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Insert the chip')
        self.create_next_button('tutorial2', disabled=True)
        self.create_back_button('chip')
        self['img'] = gui.Image(self, [400, 200],
                                'images/tuto1.png',
                                h=200)


class Tutorial2Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial3')
        self.create_back_button('tutorial1', 'Previous')
        self['img'] = gui.Image(self, [400, 200],
                                'images/tuto2.png',
                                h=200)


class Tutorial3Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial4')
        self.create_back_button('tutorial2', 'Previous')
        self['img'] = gui.Image(self, [400, 200],
                                'images/tuto3.png',
                                h=200)


class Tutorial4Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('tutorial5')
        self.create_back_button('tutorial3', 'Previous')
        self['img'] = gui.Image(self, [400, 200],
                                'images/tuto4.png',
                                h=200)


class Tutorial5Layer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_next_button('insert', 'Start')
        self.create_back_button('tutorial4', 'Previous')
        self['img'] = gui.Image(self, [400, 200],
                                'images/tuto5.png',
                                h=200)


class InsertLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Insert the chip')
        self.create_next_button('focus', 'Done')
        self.create_back_button('chip')
        # TODO create correct insert_chip.png
        self['img'] = gui.Image(self, [400, 200],
                                'images/insert_chip.png',
                                h=200)


class FocusLayer(Layer):

    # TODO: add a stream object in initGui
    def __init__(self, app):
        super().__init__(app)

        self.create_title('Set the focus')
        self.create_next_button('loading', 'Done')
        self.create_back_button('insert')
        self['stream'] = gui.Video(self, (400, 200), h=200)


class LoadingLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Please wait...')
        self.create_next_button('circle')
        self.create_back_button('focus')
        self['stream'] = gui.Video(self, (400, 200), h=200)


class ResultsLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Results')


class CircleLayer(Layer):

    def __init__(self, app):
        super().__init__(app)
        self.create_title('Please select the visible spots')
        self.create_next_button('choice', 'Done')
        self.create_back_button('loading')

        self['circles'] = gui.Group()
        self['add'] = gui.Button(self, (600, 50), (40, 40), '+',
                                 lambda: self.new_circle((100, 100), 42))
        self['rem'] = gui.Button(self, (660, 50), (40, 40), '-',
                                 lambda: self.rem_selected_circles())
        self['reset'] = gui.Button(self, (740, 50), (80, 40), 'Reset',
                                   lambda: self.set_circles([]))
        self['size'] = gui.Slider(self, (400, 340), (512, 64), 10, 200,
                                  lambda r: self.set_selected_circles_radius(r))

    def select_circle(self, c):
        for v in self['circles'].values():
            v.is_selected = False
        if c:
            c.is_selected = True
            self['size'].set(c.radius)

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

    def set_selected_circles_radius(self, r):
        for k in self.get_selected_circles():
            self['circles'][k].radius = round(r)

    def click_down(self, pos, catched):
        catched = super().click_down(pos, catched)
        if not catched:
            self.select_circle(None)
        return catched


class ProfilesLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        def nope():
            pass

        btn_list = [
            ('bourban', 'Bourban Emile', nope),
            ('conti', 'Conti Mark', nope),
            ('cucu', 'Cucu Raluca', nope),
            ('giezendanner', 'Giezendanner Ludovic', nope),
            ('perier', 'Perier Marion', nope),
            ('schalk', 'Schalk Katia', nope),
            ('viatte', 'Viatte Clara', nope),
        ]
        self.create_background()
        self.create_small_buttons_list(btn_list)
        self.create_back_button('main')


class HelpLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        def nope():
            pass

        btn_list = [
            ('bourban', 'Bourban Emile', nope),
            ('conti', 'Conti Mark', nope),
            ('cucu', 'Cucu Raluca', nope),
            ('giezendanner', 'Giezendanner Ludovic', nope),
            ('perier', 'Perier Marion', nope),
            ('schalk', 'Schalk Katia', nope),
            ('viatte', 'Viatte Clara', nope),
        ]
        self.create_background()
        self.create_small_buttons_list(btn_list)
        self.create_back_button('main')


class ParametersLayer(Layer):

    def __init__(self, app):
        super().__init__(app)

        def nope():
            pass

        btn_list = [
            ('bourban', 'Bourban Emile', nope),
            ('conti', 'Conti Mark', nope),
            ('cucu', 'Cucu Raluca', nope),
            ('giezendanner', 'Giezendanner Ludovic', nope),
            ('perier', 'Perier Marion', nope),
            ('schalk', 'Schalk Katia', nope),
            ('viatte', 'Viatte Clara', nope),
        ]
        self.create_background()
        self.create_small_buttons_list(btn_list)
        self.create_back_button('main')

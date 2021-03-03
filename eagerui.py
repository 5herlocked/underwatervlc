import kivy

kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.clearcolor = (77 / 255, 162 / 255, 180 / 255, 1)
import inspect


def photodiodeStart(pin, freq):
    print('start', pin, freq)


def photodiodeStop(pin, freq):
    print('stop', pin, freq)


def zcamStart():
    print('zcam start')


def zcamStop():
    print('zcam stop')


def rosStart():
    print('ros started')


def rosStop():
    print('ros stopped')


def transmitterStart(message, pin, freq):
    pass


def transmitterStop(message, pin, freq):
    pass


def I2Ctransmitter1Start(message, BUS, freq):
    pass


def I2Ctransmitter1Stop(message, BUS, freq):
    pass


def I2Ctransmitter2Start(message, BUS, freq):
    pass


def I2Ctransmitter2Stop(message, BUS, freq):
    pass


functions = [
    ('Photodiode', photodiodeStart, photodiodeStop),
    ('Transmitter', transmitterStart, transmitterStop),
    ('ROS Teleop Launch', rosStart, rosStop),
    ('I2C Transmitter 1', I2Ctransmitter1Start, I2Ctransmitter1Stop),
    ('Zed Cam', zcamStart, zcamStop),

    ('I2C Transmitter 2', I2Ctransmitter2Start, I2Ctransmitter2Stop),
]


class ControlUnit(BoxLayout):
    def __init__(self, name, start, stop, **kwargs):
        super(ControlUnit, self).__init__(**kwargs)

        self.startFn = start
        self.stopFn = stop

        self.orientation = 'vertical'
        self.padding = [20, 20, 20, 20]
        self.spacing = 20
        args = inspect.getfullargspec(start)[0]
        self.arguments = dict.fromkeys(args, '')
        self.fields = {}
        if args:
            self.inputs = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=30)
            for arg in args:
                f = TextInput(hint_text=arg)
                self.fields[arg] = f
                self.inputs.add_widget(f)

        self.buttons = BoxLayout(orientation='horizontal',
                                 size_hint=(1, None), height=50, spacing=30)
        start_button = Button(text='start')
        start_button.background_normal = 'bg.jpeg'
        start_button.background_color = (99 / 255, 211 / 255, 73 / 255, 1)
        start_button.bind(on_press=self.handle_start)

        stop_button = Button(text='stop')
        stop_button.background_normal = 'bg.jpeg'
        stop_button.background_color = (183 / 255, 49 / 255, 40 / 255, 1)
        stop_button.bind(on_press=self.handle_stop)

        self.buttons.add_widget(start_button)
        self.buttons.add_widget(stop_button)
        self.title = Label(text=name, size_hint=(1, 0.2), height=50, font_size=50)
        self.add_widget(self.title)

        if args:
            self.add_widget(self.inputs)

        self.add_widget(self.buttons)

    def handle_start(self, view):
        if self.fields:
            for arg in self.fields:
                self.arguments[arg] = self.fields[arg].text
            self.startFn(**self.arguments)
        else:
            self.startFn()

    def handle_stop(self, view):
        if self.fields:
            for arg in self.fields:
                self.arguments[arg] = self.fields[arg].text
            self.stopFn(**self.arguments)
        else:
            self.stopFn()


class ControlPanel(GridLayout):
    def __init__(self, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 5
        self.spacing = 30
        self.background_color = 'white'
        self.padding = [100, ] * 4
        for c in functions:
            self.add_widget(ControlUnit(c[0], c[1], c[2]))

        self.add_widget(Label(text=''))


class MyApp(App):
    def build(self):
        self.title = 'EAGER Research Dashboard'
        return ControlPanel()

    def on_start(self):
        pass

    def on_stop(self):
        pass


if __name__ == '__main__':
    MyApp().run()

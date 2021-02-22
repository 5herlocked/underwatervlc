import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from config import *
from kivy.core.window import Window


import pysftp
import sys
import signal

Config.set('graphics', 'resizable', 1)
kivy.require('2.0.0')


def terminate():
    for process in receivers:
        process.send_signal(signal.SIGTERM)
    for process in transmitters:
        process.send_signal(signal.SIGTERM)
    for process in cars:
        process.send_signal(signal.SIGTERM)
    sys.exit()


# Creating Layout class
class Trans_Receiver(GridLayout):
    def calculate(self, calculation):
        print("clicked function")
        print(calculation)

    def start_receiver(self, pin, freq, name):
        # find name in receivers use that receiver to do the thing (start receiving)
        # do the thing -> call to Receiver.start_receiver()
        for receiver in receivers:
            if name == receiver:
                receiver.start_receiver(pin, freq)
                # Kenny stated that we need to use the Class name and not the specific object

    def start_transmitter(self, pin, freq, message, name):
        for transmitter in transmitters:
            if name in transmitter.name:
                transmitter.start_transmission(pin, freq, message)

    def stop_receiver(self, name):
        for receiver in receivers:
            if name in receiver.name:
                receiver.stop_receiver()

    def stop_transmitter(self, name):
        for transmitter in transmitters:
            if name in transmitter.name:
                transmitter.stop_transmission()

    def get_receiver_log(self, name):
        for receiver in receivers:
            if name in receiver.name:
                receiver.get_receiver_log()

    def start_I2Ctranmitter(self, bus):
        pass

    def stop_12Ctransmitter(self, bus):
        pass


class CalculatorApp(App):
    def build(self):
        return Trans_Receiver()



if __name__ == "__main__":
    Window.clearcolor = (0, 1.5, 1, 1)
    instantiate_config()
    calcApp = CalculatorApp()
    calcApp.run()

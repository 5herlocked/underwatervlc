from typing import List, Any

import kivy    
from kivy.app import App     
kivy.require('1.9.0')  
from kivy.uix.gridlayout import GridLayout 
from kivy.config import Config 
Config.set('graphics', 'resizable', 1)
import subprocess
import sys
import signal

receiver_processes = []
transmitter_process = []


def terminate():
    for process in receiver_processes:
        process.send_signal(signal.SIGTERM)
    for process in transmitter_process:
        process.send_signal(signal.SIGTERM)

    sys.exit()


# Creating Layout class 
class CalcGridLayout(GridLayout): 
    def calculate(self, calculation):
        print("clicked function") 
        print(calculation)


    def start_receiver(self, pin, freq):
        receiver_processes.append(subprocess.Popen(['python3', 'receiver_basic.py', '-p', pin, '-f', freq]))


    def start_transmitter(self, pin, freq, message):
        transmitter_process.append(subprocess.Popen(['python3', 'transmitter.py', '-p', pin, '-f', freq, '-m', message]))

    
    def stop_receiver(self, number):
        receiver_processes[number].send_signal(signal.SIGTERM)


    def stop_transmitter(self, number):
        transmitter_process[number].send_signal(signal.SIGTERM)


class CalculatorApp(App): 
    def build(self): 
        return CalcGridLayout() 


calcApp = CalculatorApp() 
calcApp.run() 
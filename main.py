import kivy    
from kivy.app import App     
kivy.require('1.9.0')  
from kivy.uix.gridlayout import GridLayout 
from kivy.config import Config 
Config.set('graphics', 'resizable', 1) 
# Creating Layout class 
class CalcGridLayout(GridLayout): 
    def calculate(self, calculation):
        print("clicked function") 
        print(calculation)

class CalculatorApp(App): 
    def build(self): 
        return CalcGridLayout() 
     
calcApp = CalculatorApp() 
calcApp.run() 
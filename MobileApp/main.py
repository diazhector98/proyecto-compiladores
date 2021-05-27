import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_file("compiladores.kv")

class Compiladores(Widget):
    def __init__(self, **kwargs):
        super(Compiladores, self).__init__(**kwargs)
        
    def compile_button_pressed(self):
        self.output_text.text = "Compile pressed"

    def run_button_pressed(self):
        self.output_text.text = "Run pressed"
    

class CompiladoresApp(App):
    def build(self):
        return Compiladores()


if __name__ == '__main__':
    CompiladoresApp().run()
from kivy.app import App
from kivy.uix.widget import Widget


class Compiladores(Widget):
    pass


class CompiladoresApp(App):
    def build(self):
        return Compiladores()


if __name__ == '__main__':
    CompiladoresApp().run()
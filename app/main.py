from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.label import MDLabel

class Main(MDApp):
    def build(self):
        screen = Screen()
        label = MDLabel(text = "Eudaimonia",
                        halign = "center",
                        font_style = "H4",
                        markup = True)
        screen.add_widget(label)
        return screen

Main().run()
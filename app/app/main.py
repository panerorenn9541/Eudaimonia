from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

KV = '''
<TitleScreen>:
    name: "title"
    MDLabel:
        text: "Eudaimonia"
        halign: "center"
        font_style: "H2"
        markup: True
        bold: True

<TitleScreen2>:
    name: "title2"
    MDLabel:
        text: "First, tell us about you"
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True

<NameScreen>:
    user_name: user_name
    name: "name"
    MDLabel:
        text: "What is your name?"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True

    MDTextField:
        id: user_name
        hint_text: "Enter your name"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.name_enter()

<StatsScreen>:
    height1: height1
    weight: weight
    age: age
    name: "stats"
    MDLabel:
        text: "Enter your Biometrics"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True

    MDTextField:
        id: height1
        hint_text: "Enter your height (in CM)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True

    MDTextField:
        id: weight
        hint_text: "Enter your weight (in KG)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True

    MDTextField:
        id: age
        hint_text: "Enter your age"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint_x: None
        width: 300
        required: True

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.15}
        on_press:
            root.stats_enter()

<DietScreen>:
    restrictions: restrictions
    goals:goals
    name: "diet"
    MDLabel:
        text: "Let us know about your diet and goals"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True
        
    MDTextField:
        id: restrictions
        hint_text: "Enter any dietary restrictions you may have"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True
    
    MDTextField:
        id: goals
        hint_text: "Enter your current goals"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_press:
            root.diet_enter()        

            
<HomeScreen>:
    MDBottomNavigation:
        panel_color: .2, .2, .2, 1
        
        MDBottomNavigationItem:
            name: "home"
            text: "Home"
            
            MDLabel:
                text: "Eudaimonia"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True

        MDBottomNavigationItem:
            name: "food"
            text: "Food"

            MDLabel:
                text: "Food"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True

        MDBottomNavigationItem:
            name: "exercise"
            text: "Exercise"

            MDLabel:
                text: "Exercise"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True

        MDBottomNavigationItem:
            name: "sleep"
            text: "Sleep"

            MDLabel:
                text: "Sleep"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True

<FoodScreen>:
    name: "food"
    MDLabel:
        text: "Food"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
<ExerciseScreen>:
    name: "exercise"
    MDLabel:
        text: "Exercise"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
<SleepScreen>:
    name: "sleep"
    MDLabel:
        text: "Sleep"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True

<Manager>:
    TitleScreen:
        name: "title"
    TitleScreen2:
        name: "title2"
    NameScreen:
        name: "name"
    StatsScreen:
        name: "stats"
    DietScreen:
        name: "diet"
    HomeScreen:
        name: "home"
    FoodScreen:
        name: "food"
    ExerciseScreen:
        name: "exercise"
    SleepScreen:
        name: "sleep"
'''

Builder.load_string(KV)


class Manager(ScreenManager):
    pass


class TitleScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, scr):
        self.parent.current = "title2"


class TitleScreen2(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, scr):
        self.parent.current = "name"


class NameScreen(Screen):
    def name_enter(self):
        self.user_name = self.user_name.text
        self.parent.current = "stats"


class StatsScreen(Screen):
    def stats_enter(self):
        self.height1 = self.height1.text
        self.weight = self.weight.text
        self.age = self.age.text
        self.parent.current = "diet"


class DietScreen(Screen):
    def diet_enter(self):
        self.restrictions = self.restrictions.text
        self.goals = self.goals.text
        self.parent.current = "home"


class HomeScreen(Screen):
    pass


class FoodScreen(Screen):
    pass


class ExerciseScreen(Screen):
    pass


class SleepScreen(Screen):
    pass


class Main(MDApp):
    def build(self):
        return Manager()


if __name__ == '__main__':
    Main().run()

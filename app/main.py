from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from plyer import notification

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
    name: "diet"
    MDLabel:
        text: "Let us know about your dietary restrictions"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.7}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_lactose()
        
    MDLabel:
        text: "Lactose Intolerance"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.7}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_vegan()
        
    MDLabel:
        text: "Vegetarian or Vegan"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.6}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.5}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_pescetarian()
        
    MDLabel:
        text: "Pescetarian"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.5}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_peanut()
        
    MDLabel:
        text: "Peanut Allergies"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.4}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.3}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_gluten()
        
    MDLabel:
        text: "Gluten Intolerance"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.3}
        markup: True
        bold: False
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.1}
        on_press:
            root.diet_enter()

<GoalsScreen>:
    name: "goals"
    MDLabel:
        text: "Let us know about some of your goals"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.7}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_lose_weight()
        
    MDLabel:
        text: "Lose Weight"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.7}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_gain_muscle()
        
    MDLabel:
        text: "Gain Muscle"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.6}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.5}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_wake_up()
        
    MDLabel:
        text: "Wake Up Early"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.5}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_plant_food()
        
    MDLabel:
        text: "Eat More Plant Based Foods"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.4}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.3}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_sugar()
        
    MDLabel:
        text: "Cut Down On Sugar"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.3}
        markup: True
        bold: False
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.1}
        on_press:
            root.goals_enter()
            
<WelcomeScreen>:
    name: "welcome"
    MDLabel:
        text: "Welcome to Eudaimonia"
        halign: "center"
        font_style: "H2"
        markup: True
        bold: True

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
            
            Image:
                source: 'images\eudaimoniaLogo.png'
                pos_hint:{'center_y' : 0.4}

        MDBottomNavigationItem:
            name: "food"
            text: "Food"
            
            Image:
                source: 'images\eplate.png'
                pos_hint:{'center_y': 0.3}

            MDLabel:
                text: "Food"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDTextButton:
                text: "Enter Your Meals ->"
                pos_hint:{'center_x' : 0.9, 'center_y': 0.8}
                on_press:
                    root.enter_meals()

        MDBottomNavigationItem:
            name: "exercise"
            text: "Exercise"
            
            Image:
                source: 'images\eweight.png'
                pos_hint:{'center_y': 0.3, 'center_x': 0.5}
                size_hint_x: 0.5
                size_hint_y: 0.5

            MDLabel:
                text: "Exercise"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDTextButton:
                text: "Enter Your Workouts ->"
                pos_hint:{'center_x' : 0.88, 'center_y': 0.8}
                on_press:
                    root.enter_exercise()

        MDBottomNavigationItem:
            name: "sleep"
            text: "Sleep"
            
            Image:
                source: 'images\ebed.png'
                pos_hint:{'center_y': 0.3, 'center_x': 0.5}
                size_hint_x: 0.8
                size_hint_y: 0.8

            MDLabel:
                text: "Sleep"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDTextButton:
                text: "Enter Your Sleep Times ->"
                pos_hint:{'center_x' : 0.87, 'center_y': 0.8}
                on_press:
                    root.enter_sleep()

<FoodScreen>:
    meal: meal
    name: "food_entry"
    MDLabel:
        text: "Food"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
    MDTextField:
        id: meal
        hint_text: "Enter your meal"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.food_enter()
        
<ExerciseScreen>:
    workout: workout
    name: "exercise_entry"
    MDLabel:
        text: "Exercise"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
    MDTextField:
        id: workout
        hint_text: "Enter your workout"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        on_press:
            root.exercise_enter()
        
<SleepScreen>:
    sleep_start: sleep_start
    sleep_end: sleep_end
    name: "sleep_entry"
    MDLabel:
        text: "Sleep"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
    MDTextField:
        id: sleep_start
        hint_text: "Enter when you went to sleep"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True
        
    MDTextField:
        id: sleep_end
        hint_text: "Enter when you woke up"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_press:
            root.sleep_enter()

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
    GoalsScreen:
        name: "goals"
    WelcomeScreen:
        name: "welcome"
    HomeScreen:
        name: "home"
    FoodScreen:
        name: "food_entry"
    ExerciseScreen:
        name: "exercise_entry"
    SleepScreen:
        name: "sleep_entry"
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
        self.parent.current = "goals"

    def toggle_vegan(self):
        '''***NEED TO CHANGE TO A TOGGLE INSTEAD OF SETTING TRUE***  MAKE A USER CLASS'''
        self.vegan = True

    def toggle_lactose(self):
        self.lactose = True

    def toggle_peanut(self):
        self.peanut = True

    def toggle_gluten(self):
        self.gluten = True

    def toggle_pescetarian(self):
        self.pescetarian = True


class GoalsScreen(Screen):
    def goals_enter(self):
        self.parent.current = "welcome"

    def toggle_lose_weight(self):
        self.lose_weight = True

    def toggle_gain_muscle(self):
        self.gain_muscle = True

    def toggle_wake_up(self):
        self.wake_up = True

    def toggle_plant_food(self):
        self.plant_food = True

    def toggle_sugar(self):
        self.sugar = True


class WelcomeScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, scr):
        self.parent.current = "home"


class HomeScreen(Screen):
    def enter_meals(self):
        self.parent.current = "food_entry"

    def enter_exercise(self):
        self.parent.current = "exercise_entry"

    def enter_sleep(self):
        self.parent.current = "sleep_entry"


class FoodScreen(Screen):
    def food_enter(self):
        self.meal = self.meal.text
        self.parent.current = "home"


class ExerciseScreen(Screen):
    def exercise_enter(self):
        self.workout = self.workout.text
        self.parent.current = "home"


class SleepScreen(Screen):
    def sleep_enter(self):
        self.sleep_start = self.sleep_start.text
        self.sleep_end = self.sleep_end.text
        self.parent.current = "home"


class Main(MDApp):
    def build(self):
        return Manager()


if __name__ == '__main__':
    Main().run()

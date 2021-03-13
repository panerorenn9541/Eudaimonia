from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDRoundFlatButton
from kivy.core.window import Window
import exercise_score
import exercise as ex
import database
from plyer import notification
import datetime

es = exercise_score.ExerciseScore(5, 5, 5, [])

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
        pos_hint:{'center_x': 0.5, 'center_y': 0.1}
        on_press:
            root.stats_enter()
            
<GeneralScreen>:
    workout_freq:workout_freq
    sleep_hours:sleep_hours
    name: "general"
    MDLabel:
        text: "Some general information"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True
        
    MDTextField:
        id: workout_freq
        hint_text: "How many days do you workout per week?"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        required: True
        
    MDTextField:
        id: sleep_hours
        hint_text: "How many hours do you sleep per night?"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: 300
        required: True
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_press:
            root.general_enter()
            
<GenderScreen>:
    name: "gender"
    MDLabel:
        text: "A bit about your gender"
        halign: "center"
        pos_hint:{'center_y': 0.9}
        font_style: "H4"
        markup: True
        bold: True
        
    MDCheckbox:
        group: "gender"
        pos_hint:{'center_x' : 0.2, 'center_y': 0.7}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_male()
        
    MDLabel:
        text: "Male"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.7}
        markup: True
        bold: False
        
    MDCheckbox:
        group: "gender"
        pos_hint:{'center_x' : 0.2, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_female()
        
    MDLabel:
        text: "Female"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.6}
        markup: True
        bold: False
        
    MDCheckbox:
        group: "gender"
        pos_hint:{'center_x' : 0.2, 'center_y': 0.5}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_lactating()
        
    MDLabel:
        text: "Lactating Female"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.5}
        markup: True
        bold: False
        
    MDCheckbox:
        group: "gender"
        pos_hint:{'center_x' : 0.2, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_pregnant()
        
    MDLabel:
        text: "Pregnant Female"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.4}
        markup: True
        bold: False
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.1}
        on_press:
            root.gender_enter()

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
        text: "Vegan"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.6}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.5}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_vegetarian()
        
    MDLabel:
        text: "Vegetarian"
        halign: "center"
        pos_hint:{'center_x' : 0.5, 'center_y': 0.5}
        markup: True
        bold: False
        
    MDCheckbox:
        pos_hint:{'center_x' : 0.2, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_pescetarian()
        
    MDLabel:
        text: "Pescetarian"
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
    home:home
    food:food
    exercise:exercise
    sleep:sleep
    MDBottomNavigation:
        panel_color: .2, .2, .2, 1
        
        MDBottomNavigationItem:
            id:home
            name: "home"
            text: "Home"
            on_enter:
                root.home_enter()
            
            MDLabel:
                text: "Eudaimonia"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDLabel:
                text: "Individual Scores"
                pos_hint:{'center_y': 0.4}
                halign: "center"
                font_style: "H6"
                markup: True
                bold: True
                
            MDLabel:
                text: "Food:"
                pos_hint:{'center_x':0.2,'center_y': 0.25}
                halign: "center"
                font_style: "H6"
                markup: True
                bold: False
                
            MDLabel:
                text: "Exercise:"
                pos_hint:{'center_x':0.5,'center_y': 0.25}
                halign: "center"
                font_style: "H6"
                markup: True
                bold: False
                
            MDLabel:
                text: "Sleep:"
                pos_hint:{'center_x':0.8,'center_y': 0.25}
                halign: "center"
                font_style: "H6"
                markup: True
                bold: True
            
            #Image:
                #source: 'images\eudaimoniaLogo.png'
                #pos_hint:{'center_y' : 0.4}

        MDBottomNavigationItem:
            id:food
            name: "food"
            text: "Food"
            on_enter:
                root.food_enter()
            
            #Image:
                #source: 'images\eplate.png'
                #pos_hint:{'center_y': 0.3}

            MDLabel:
                text: "Food"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDLabel:
                text: "Your Food Score is: "
                pos_hint:{'center_y': 0.75, 'center_x' : 0.5}
                halign:"center"
                markup:True
                bold:True
                font_style:"H5"
                
            MDRoundFlatIconButton:
                text: "Enter Meals"
                size_hint: None, None
                size: 125,35
                pos_hint:{'center_x' : 0.9, 'center_y': 0.8}
                on_press:
                    root.enter_meals()
                icon: "silverware-fork-knife"

        MDBottomNavigationItem:
            id:exercise
            name: "exercise"
            text: "Exercise"
            on_enter:
                root.exercise_enter()
            
            #Image:
                #source: 'images\eweight.png'
                #pos_hint:{'center_y': 0.3, 'center_x': 0.5}
                #size_hint_x: 0.5
                #size_hint_y: 0.5

            MDLabel:
                text: "Exercise"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDLabel:
                text: "Your Exercise Score is: "
                pos_hint:{'center_y': 0.75, 'center_x' : 0.5}
                halign:"center"
                markup:True
                bold:True
                font_style:"H5"
                
            MDRoundFlatIconButton:
                text: "Enter Workouts"
                size_hint: None, None
                size: 150,35
                pos_hint:{'center_x' : 0.9, 'center_y': 0.8}
                on_press:
                    root.enter_exercise()
                icon: "dumbbell"

        MDBottomNavigationItem:
            id:sleep
            name: "sleep"
            text: "Sleep"
            on_enter:
                root.sleep_enter()
            
            #Image:
                #source: 'images\ebed.png'
                #pos_hint:{'center_y': 0.3, 'center_x': 0.5}
                #size_hint_x: 0.8
                #size_hint_y: 0.8

            MDLabel:
                text: "Sleep"
                pos_hint:{'center_y': 0.9}
                halign: "center"
                font_style: "H4"
                markup: True
                bold: True
                
            MDLabel:
                text: "Your Sleep Score is: "
                pos_hint:{'center_y': 0.75, 'center_x' : 0.5}
                halign:"center"
                markup:True
                bold:True
                font_style:"H5"
                
            MDRoundFlatIconButton:
                text: "Enter Sleep"
                size_hint: None, None
                size: 125,35
                pos_hint:{'center_x' : 0.9, 'center_y': 0.8}
                on_press:
                    root.enter_sleep()
                icon: "bed-king"

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
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        size_hint_x: None
        width: 300
        required: True

    MDRoundFlatIconButton:
        text: "Back"
        icon:"skip-backward"
        size_hint: None, None
        size: 90,35
        pos_hint:{'center_x': 0.1, 'center_y': 0.9}
        on_press:
            root.food_back()

    MDRoundFlatIconButton:
        text: "Search"
        icon:"account-search"
        size_hint: None, None
        size: 110,35
        pos_hint:{'center_x': 0.77, 'center_y': 0.75}
        on_press:
            root.food_enter()
            
<FinalFoodScreen>:
    name: "final_food"
    month:month
    day:day
    year:year
    hour:hour
    minute:minute
    am:am
    pm:pm
    yes:yes
    soso:soso
    no:no
    breakfast:breakfast
    lunch:lunch
    dinner:dinner
    snack:snack
    MDLabel:
        text: "Food"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
    MDLabel:
        text: "Did you enjoy your meal?"
        pos_hint:{'center_y': 0.75}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: yes
        group: "like"
        pos_hint:{'center_x' : 0.25, 'center_y': 0.65}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_yes()
        
    MDLabel:
        text: "Yes"
        halign: "center"
        pos_hint:{'center_x' : 0.3, 'center_y': 0.65}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: soso
        group: "like"
        pos_hint:{'center_x' : 0.45, 'center_y': 0.65}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_soso()
        
    MDLabel:
        text: "So-so"
        halign: "center"
        pos_hint:{'center_x' : 0.51, 'center_y': 0.65}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: no
        group: "like"
        pos_hint:{'center_x' : 0.65, 'center_y': 0.65}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_no()
        
    MDLabel:
        text: "No"
        halign: "center"
        pos_hint:{'center_x' : 0.7, 'center_y': 0.65}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDLabel:
        text: "When did you eat your meal?"
        pos_hint:{'center_y': 0.5}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDRectangleFlatIconButton:
        text: "Now"
        icon: "clock"
        size_hint: None, None
        size: 90,35
        pos_hint:{'center_x': 0.8, 'center_y': 0.5}
        on_press:
            root.now_time()

    MDTextField:
        id: month
        hint_text: "Month"
        pos_hint: {'center_x': 0.1, 'center_y': 0.4}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: day
        hint_text: "Day"
        pos_hint: {'center_x': 0.25, 'center_y': 0.4}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: year
        hint_text: "Year"
        pos_hint: {'center_x': 0.4, 'center_y': 0.4}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: hour
        hint_text: "Hour"
        pos_hint: {'center_x': 0.55, 'center_y': 0.4}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: minute
        hint_text: "Minute"
        pos_hint: {'center_x': 0.7, 'center_y': 0.4}
        size_hint_x: None
        width: 60
        required: True
        
    MDCheckbox:
        id:am
        group: "ampm"
        pos_hint:{'center_x' : 0.8, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_am()
        
    MDLabel:
        text: "AM"
        halign: "center"
        pos_hint:{'center_x' : 0.84, 'center_y': 0.4}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id:pm
        group: "ampm"
        pos_hint:{'center_x' : 0.9, 'center_y': 0.4}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_pm()
        
    MDLabel:
        text: "PM"
        halign: "center"
        pos_hint:{'center_x' : 0.94, 'center_y': 0.4}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDLabel:
        text: "What did you eat this meal for?"
        pos_hint:{'center_y': 0.25}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: breakfast
        group: "type"
        pos_hint:{'center_x' : 0.15, 'center_y': 0.15}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_breakfast()
        
    MDLabel:
        text: "Breakfast"
        halign: "center"
        pos_hint:{'center_x' : 0.22, 'center_y': 0.15}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: lunch
        group: "type"
        pos_hint:{'center_x' : 0.35, 'center_y': 0.15}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_lunch()
        
    MDLabel:
        text: "Lunch"
        halign: "center"
        pos_hint:{'center_x' : 0.40, 'center_y': 0.15}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: dinner
        group: "type"
        pos_hint:{'center_x' : 0.55, 'center_y': 0.15}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_dinner()
        
    MDLabel:
        text: "Dinner"
        halign: "center"
        pos_hint:{'center_x' : 0.6, 'center_y': 0.15}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: snack
        group: "type"
        pos_hint:{'center_x' : 0.75, 'center_y': 0.15}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_snack()
        
    MDLabel:
        text: "Snack"
        halign: "center"
        pos_hint:{'center_x' : 0.8, 'center_y': 0.15}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.05}
        on_press:
            root.final_food_enter()
        
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
        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
        size_hint_x: None
        width: 300
        required: True
        
    MDRoundFlatIconButton:
        text: "Back"
        icon:"skip-backward"
        size_hint: None, None
        size: 90,35
        pos_hint:{'center_x': 0.1, 'center_y': 0.9}
        on_press:
            root.exercise_back()

    MDRoundFlatIconButton:
        text: "Search"
        icon:"account-search"
        size_hint: None, None
        size: 110,35
        pos_hint:{'center_x': 0.77, 'center_y': 0.75}
        on_press:
            root.exercise_enter()
        
<SleepScreen>:
    sleep_hour:sleep_hour
    sleep_minute: sleep_minute
    sleep_am:sleep_am
    sleep_pm:sleep_pm
    wakeup_hour:wakeup_hour
    wakeup_minute:wakeup_minute
    wakeup_am:wakeup_am
    wakeup_pm:wakeup_pm
    well:well
    soso:soso
    bad:bad
    name: "sleep_entry"
    MDLabel:
        text: "Sleep"
        pos_hint:{'center_y': 0.9}
        halign: "center"
        font_style: "H4"
        markup: True
        bold: True
        
    MDLabel:
        text: "When did you go to sleep last night?"
        pos_hint:{'center_y': 0.75, 'center_x' : 0.22}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDTextField:
        id: sleep_hour
        hint_text: "Hour"
        pos_hint: {'center_x': 0.08, 'center_y': 0.6}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: sleep_minute
        hint_text: "Minute"
        pos_hint: {'center_x': 0.17, 'center_y': 0.6}
        size_hint_x: None
        width: 60
        required: True
        
    MDCheckbox:
        id:sleep_am
        group: "sleep_ampm"
        pos_hint:{'center_x' : 0.25, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_sleep_am()
        
    MDLabel:
        text: "AM"
        halign: "center"
        pos_hint:{'center_x' : 0.29, 'center_y': 0.6}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id:sleep_pm
        group: "sleep_ampm"
        pos_hint:{'center_x' : 0.35, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_sleep_pm()
        
    MDLabel:
        text: "PM"
        halign: "center"
        pos_hint:{'center_x' : 0.39, 'center_y': 0.6}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDLabel:
        text: "When did you wake up this morning?"
        pos_hint:{'center_y': 0.75, 'center_x' : 0.78}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDRectangleFlatIconButton:
        text: "Now"
        icon: "clock"
        size_hint: None, None
        size: 90,35
        pos_hint:{'center_x': 0.78, 'center_y': 0.5}
        on_press:
            root.now_time()
        
    MDTextField:
        id: wakeup_hour
        hint_text: "Hour"
        pos_hint: {'center_x': 0.64, 'center_y': 0.6}
        size_hint_x: None
        width: 60
        required: True
        
    MDTextField:
        id: wakeup_minute
        hint_text: "Minute"
        pos_hint: {'center_x': 0.73, 'center_y': 0.6}
        size_hint_x: None
        width: 60
        required: True
        
    MDCheckbox:
        id:wakeup_am
        group: "wakeup_ampm"
        pos_hint:{'center_x' : 0.81, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_wakeup_am()
        
    MDLabel:
        text: "AM"
        halign: "center"
        pos_hint:{'center_x' : 0.85, 'center_y': 0.6}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id:wakeup_pm
        group: "wakeup_ampm"
        pos_hint:{'center_x' : 0.91, 'center_y': 0.6}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_wakeup_pm()
        
    MDLabel:
        text: "PM"
        halign: "center"
        pos_hint:{'center_x' : 0.95, 'center_y': 0.6}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDLabel:
        text: "How did you sleep last night?"
        pos_hint:{'center_y': 0.4}
        halign:"center"
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: well
        group: "like"
        pos_hint:{'center_x' : 0.25, 'center_y': 0.3}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_well()
        
    MDLabel:
        text: "Well"
        halign: "center"
        pos_hint:{'center_x' : 0.3, 'center_y': 0.3}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: soso
        group: "like"
        pos_hint:{'center_x' : 0.45, 'center_y': 0.3}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_soso()
        
    MDLabel:
        text: "So-so"
        halign: "center"
        pos_hint:{'center_x' : 0.51, 'center_y': 0.3}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDCheckbox:
        id: bad
        group: "like"
        pos_hint:{'center_x' : 0.65, 'center_y': 0.3}
        size_hint: None, None
        size: dp(70), dp(70)
        on_active:
            root.toggle_bad()
        
    MDLabel:
        text: "Bad"
        halign: "center"
        pos_hint:{'center_x' : 0.7, 'center_y': 0.3}
        markup:True
        bold:False
        size:0.2, 0.075
        
    MDRoundFlatIconButton:
        text: "Back"
        icon:"skip-backward"
        size_hint: None, None
        size: 90,35
        pos_hint:{'center_x': 0.1, 'center_y': 0.9}
        on_press:
            root.sleep_back()

    MDRectangleFlatButton:
        text: "Done"
        pos_hint:{'center_x': 0.5, 'center_y': 0.1}
        on_press:
            root.sleep_enter()

<Manager>:
    #HomeScreen:
     #   name: "home"
    TitleScreen:
        name: "title"
    TitleScreen2:
        name: "title2"
    NameScreen:
        name: "name"
    StatsScreen:
        name: "stats"
    GeneralScreen:
        name: "general"
    GenderScreen:
        name: "gender"
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
    FinalFoodScreen:
        name: "final_food"
    ExerciseScreen:
        name: "exercise_entry"
    SleepScreen:
        name: "sleep_entry"
'''

Builder.load_string(KV)


class Sleep:
    def __init__(self, sleep_time, wakeup_time, rating):
        self.sleep_time = sleep_time
        self.wakeup_time = wakeup_time
        self.rating = rating

    def get_rating(self):
        return self.rating

    def get_sleep_time(self):
        return self.sleep_time

    def get_wakeup_time(self):
        return self.wakeup_time


class User:
    def __init__(self):
        self.user_name = ""
        self.user_height = 0.0
        self.weight = 0.0
        self.age = 0
        self.workout_freq = 0.0
        self.sleep_hours = 0
        self.gender_status = ""
        self.vegan = False
        self.lactose = False
        self.vegetarian = False
        self.gluten = False
        self.pescetarian = False
        self.lose_weight = False
        self.gain_muscle = False
        self.wake_up = False
        self.plant_food = False
        self.sugar = False
        self.food_recommendation = ""
        self.exercise_recommendation = ""
        self.food_score = 0
        self.sleeps = []

    def get_name(self):
        return self.user_name

    def get_height(self):
        return self.user_height

    def get_weight(self):
        return self.weight

    def get_age(self):
        return self.age

    def get_freq(self):
        return self.workout_freq

    def get_hours(self):
        return self.sleep_hours

    def get_gender_status(self):
        return self.gender_status

    def get_vegan(self):
        return self.vegan

    def get_lactose(self):
        return self.lactose

    def get_vegetarian(self):
        return self.vegetarian

    def get_gluten(self):
        return self.gluten

    def get_pescetarian(self):
        return self.pescetarian

    def get_lose_weight(self):
        return self.lose_weight

    def get_gain_muscle(self):
        return self.gain_muscle

    def get_wake_up(self):
        return self.wake_up

    def get_plant_food(self):
        return self.plant_food

    def get_sugar(self):
        return self.sugar

    def set_name(self, new_name):
        self.user_name = new_name

    def set_height(self, new_height):
        self.user_height = new_height

    def set_weight(self, new_weight):
        self.weight = new_weight

    def set_age(self, new_age):
        self.age = new_age

    def set_freq(self, freq):
        self.workout_freq = freq

    def set_hours(self, hrs):
        self.sleep_hours = hrs

    def set_gender(self, g):
        self.gender_status = g

    def toggle_vegan(self):
        self.vegan = not self.vegan

    def toggle_lactose(self):
        self.lactose = not self.lactose

    def toggle_vegetarian(self):
        self.vegetarian = not self.vegetarian

    def toggle_gluten(self):
        self.gluten = not self.gluten

    def toggle_pescetarian(self):
        self.pescetarian = not self.pescetarian

    def toggle_lose_weight(self):
        self.lose_weight = not self.lose_weight

    def toggle_gain_muscle(self):
        self.gain_muscle = not self.gain_muscle

    def toggle_wake_up(self):
        self.wake_up = not self.wake_up

    def toggle_plant_food(self):
        self.plant_food = not self.plant_food

    def toggle_sugar(self):
        self.sugar = not self.sugar

    def enter_sleep(self, sleep):
        self.sleeps.append(sleep)

    def get_food_score(self):
        return self.food_score

    def get_exercise_recommendation(self):
        return self.exercise_recommendation

    def get_food_recommendation(self):
        return self.food_recommendation

    def set_food_score(self, scr):
        self.food_score = scr

    def set_exercise_recommendation(self, rec):
        self.exercise_recommendation = rec

    def set_food_recommendation(self, fd):
        self.food_recommendation = fd

    def get_sleep_score(self):
        total = abs(self.sleep_hours-8)
        for i in range(len(self.sleeps)):
            sleep_length = self.sleeps[i].get_wakeup_time() - self.sleeps[i].get_sleep_time()
            sleep_hours = sleep_length.seconds//3600
            total += abs(sleep_hours-8)
        avg = total/(len(self.sleeps)+1)
        intavg = int(avg)
        return abs(10-intavg)

    def get_sleep_recommendation(self):
        if len(self.sleeps) == 0:
            if self.get_wake_up():
                return "10"
            else:
                return "11"
        else:
            total_bed_time = 0
            for i in range(len(self.sleeps)):
                total_bed_time += self.sleeps[i].get_sleep_time().hour
            avg_bed_time = int(total_bed_time/len(self.sleeps))
            if avg_bed_time >= 20 and avg_bed_time <= 24:
                return str(avg_bed_time-12)
            elif self.sleeps[-1].get_rating() == "well":
                return str(self.sleeps[-1].get_sleep_time().hour-12)
            else:
                return "11"

    def get_sleep_notes(self):
        if len(self.sleeps) > 0 and self.sleeps[-1].get_rating() == "bad":
            return "Try going to bed earlier tonight and sleeping on your back"

        total = self.sleep_hours
        avg = 0
        for i in range(len(self.sleeps)):
            sleep_length = self.sleeps[i].get_wakeup_time() - self.sleeps[i].get_sleep_time()
            sleep_hours = sleep_length.seconds//3600
            total += sleep_hours
            avg = total/(len(self.sleeps)+1)
        if avg >= 10:
            return "Try setting up an alarm tonight so that you wake up earlier"
        elif avg <= 6:
            return "Try going to bed earlier tonight so that you get enough sleep"

user = User()
exercise = exercise_score.ExerciseScore()
exercise2 = ex.ExerciseDatabase()
food = database.Database()


class Manager(ScreenManager):
    pass


class TitleScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 5)

    def change_screen(self, scr):
        self.parent.current = "title2"


class TitleScreen2(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, scr):
        self.parent.current = "name"


class NameScreen(Screen):
    def name_enter(self):
        global user
        user.set_name(self.user_name.text)
        self.parent.current = "stats"


class StatsScreen(Screen):
    def stats_enter(self):
        global user
        user.set_height(float(self.height1.text))
        user.set_weight(float(self.weight.text))
        user.set_age(int(self.age.text))
        self.parent.current = "general"


class GeneralScreen(Screen):
    def general_enter(self):
        global user
        user.set_freq(int(self.workout_freq.text))
        user.set_hours(int(self.sleep_hours.text))
        self.parent.current = "gender"


class GenderScreen(Screen):
    def gender_enter(self):
        self.parent.current = "diet"

    def toggle_male(self):
        global user
        user.set_gender("Male")

    def toggle_female(self):
        global user
        user.set_gender("Female")

    def toggle_lactating(self):
        global user
        user.set_gender("Lactation")

    def toggle_pregnant(self):
        global user
        user.set_gender("Pregnant")


class DietScreen(Screen):
    def diet_enter(self):
        self.parent.current = "goals"

    def toggle_vegan(self):
        global user
        user.toggle_vegan()

    def toggle_lactose(self):
        global user
        user.toggle_lactose()

    def toggle_vegetarian(self):
        global user
        user.toggle_vegetarian()

    def toggle_gluten(self):
        global user
        user.toggle_gluten()

    def toggle_pescetarian(self):
        global user
        user.toggle_pescetarian()


class GoalsScreen(Screen):
    def goals_enter(self):
        self.parent.current = "welcome"

    def toggle_lose_weight(self):
        global user
        user.toggle_lose_weight()

    def toggle_gain_muscle(self):
        global user
        user.toggle_gain_muscle()

    def toggle_wake_up(self):
        global user
        user.toggle_wake_up()

    def toggle_plant_food(self):
        global user
        user.toggle_plant_food()

    def toggle_sugar(self):
        global user
        user.toggle_sugar()


class WelcomeScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, scr):
        global user
        global exercise
        global food

        exercise_goals = []
        if user.get_lose_weight():
            exercise_goals.append("Lose Weight")
        if user.get_gain_muscle():
            exercise_goals.append("Gain Muscle")
        exercise.__init__(user.get_freq(), user.get_height(), user.get_weight(), exercise_goals)

        food.__init__(age=user.get_age(), status=user.get_gender_status())
        if user.get_vegan() or user.get_lactose():
            food.input_food_restriction(1002)
            food.input_food_restriction(1004)
            food.input_food_restriction(1006)
            food.input_food_restriction(1008)
            food.input_food_restriction(1202)
            food.input_food_restriction(1204)
            food.input_food_restriction(1206)
            food.input_food_restriction(1208)
            food.input_food_restriction(1402)
            food.input_food_restriction(1404)
            food.input_food_restriction(1602)
            food.input_food_restriction(1604)
            food.input_food_restriction(1820)
            food.input_food_restriction(1822)
            food.input_food_restriction(5802)
            food.input_food_restriction(8002)
            food.input_food_restriction(8006)
            food.input_food_restriction(8008)

        if user.get_vegan() or user.get_vegetarian() or user.get_pescetarian():
            food.input_food_restriction(2002)
            food.input_food_restriction(2004)
            food.input_food_restriction(2006)
            food.input_food_restriction(2008)
            food.input_food_restriction(2010)
            food.input_food_restriction(2202)
            food.input_food_restriction(2204)
            food.input_food_restriction(2206)
            food.input_food_restriction(2602)
            food.input_food_restriction(2604)
            food.input_food_restriction(2606)
            food.input_food_restriction(2608)
            food.input_food_restriction(3002)
            food.input_food_restriction(3004)
            food.input_food_restriction(3702)

        if user.get_vegan() or user.get_vegetarian():
            food.input_food_restriction(2402)
            food.input_food_restriction(2404)
            food.input_food_restriction(3006)

        if user.get_vegan():
            food.input_food_restriction(2502)
            food.input_food_restriction(8010)
            food.input_food_restriction(8802)

        if user.get_gluten():
            food.input_food_restriction(3204)
            food.input_food_restriction(3208)
            food.input_food_restriction(3402)
            food.input_food_restriction(3406)
            food.input_food_restriction(3502)
            food.input_food_restriction(3504)
            food.input_food_restriction(3708)
            food.input_food_restriction(3722)
            food.input_food_restriction(4004)
            food.input_food_restriction(4202)
            food.input_food_restriction(4204)
            food.input_food_restriction(4206)
            food.input_food_restriction(4208)
            food.input_food_restriction(4402)
            food.input_food_restriction(4404)
            food.input_food_restriction(4602)
            food.input_food_restriction(4604)
            food.input_food_restriction(4802)
            food.input_food_restriction(4804)
            food.input_food_restriction(5008)
            food.input_food_restriction(5202)
            food.input_food_restriction(5204)
            food.input_food_restriction(5402)
            food.input_food_restriction(5502)
            food.input_food_restriction(5504)
            food.input_food_restriction(5506)
            food.input_food_restriction(6489)
            food.input_food_restriction(7502)

        if user.get_gluten() or user.get_lactose():
            food.input_food_restriction(3206)
            food.input_food_restriction(3602)
            food.input_food_restriction(3720)

        if user.get_vegan() or user.get_vegetarian() or user.get_pescetarian() or user.get_gluten():
            food.input_food_restriction(3702)
            food.input_food_restriction(3703)
            food.input_food_restriction(3704)

        if user.get_vegan() or user.get_gluten():
            food.input_food_restriction(3706)
            food.input_food_restriction(8412)

        if user.get_vegan() or user.get_gluten() or user.get_vegetarian():
            food.input_food_restriction(3730)

        food.input_food_log(1104493, datetime.datetime.now(), "Breakfast", 1)

        self.food_type = "Snack"
        dt = datetime.datetime.now()
        if dt.hour <= 10:
            self.food_type = "Breakfast"
        elif dt.hour <= 16:
            self.food_type = "Lunch"
        else:
            self.food_type = "Dinner"
        user.set_food_score(food.grade())
        user.set_food_recommendation(food.recommend(self.food_type))
        user.set_exercise_recommendation(exercise.get_exercise_recommendation())

        self.parent.current = "home"


home_labels = []
home_food_labels = []
home_exercise_labels = []
home_sleep_labels = []


class HomeScreen(Screen):
    def on_enter(self):
        # food.input_food_log(1104493, datetime.datetime.now(), "Breakfast", 1)
        self.food_enter()
        self.home_enter()
        self.exercise_enter()
        self.sleep_enter()

    def enter_meals(self):
        self.parent.current = "food_entry"

    def enter_exercise(self):
        self.parent.current = "exercise_entry"

    def enter_sleep(self):
        self.parent.current = "sleep_entry"

    def home_enter(self):
        global home_labels
        global food
        global exercise
        global user
        for i in range(len(home_labels)):
            self.home.remove_widget(home_labels[i])

        first_label = MDLabel(
            text="Hello " + user.get_name() + ", your current Health Score is: ",
            pos_hint={'center_y': 0.75, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H5"
        )
        self.home.add_widget(first_label)
        home_labels.append(first_label)

        food_score = user.get_food_score()[0] * 10
        intfood_score = int(food_score)
        food_label = MDLabel(
            text=str(intfood_score),
            pos_hint={'center_y': 0.15, 'center_x': 0.2},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.home.add_widget(food_label)
        home_labels.append(food_label)

        exercise.update_score()
        ex_score = exercise.get_score()
        intex_score = int(ex_score)
        exercise_label = MDLabel(
            text=str(intex_score),
            pos_hint={'center_y': 0.15, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.home.add_widget(exercise_label)
        home_labels.append(exercise_label)

        sleep_score = user.get_sleep_score()
        sleep_label = MDLabel(
            text=str(sleep_score),
            pos_hint={'center_y': 0.15, 'center_x': 0.8},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.home.add_widget(sleep_label)
        home_labels.append(sleep_label)

        total = (sleep_score+ex_score+food_score)/3
        inttotal = int(total)
        total_label = MDLabel(
            text=str(inttotal),
            pos_hint={'center_y': 0.6, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H1"
        )
        self.home.add_widget(total_label)
        home_labels.append(total_label)

    def food_enter(self):
        global home_food_labels
        global food
        for i in range(len(home_food_labels)):
            self.food.remove_widget(home_food_labels[i])

        self.food_type = "Snack"
        dt = datetime.datetime.now()
        if dt.hour <= 10:
            self.food_type = "Breakfast"
        elif dt.hour <= 16:
            self.food_type = "Lunch"
        else:
            self.food_type = "Dinner"
        first_recommendation_label = MDLabel(
            text=user.get_name() + "\'s " + self.food_type + " recommendation for today is: ",
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=False,
            font_style="H5"
        )
        self.food.add_widget(first_recommendation_label)
        home_food_labels.append(first_recommendation_label)

        recommendation = user.get_food_recommendation()
        second_recommendation_label = MDLabel(
            text="*" + recommendation[0].description + "*",
            pos_hint={'center_y': 0.35, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H5"
        )
        self.food.add_widget(second_recommendation_label)
        home_food_labels.append(second_recommendation_label)

        food_score = user.get_food_score()[0] * 10
        intfood_score = int(food_score)
        food_label = MDLabel(
            text=str(intfood_score),
            pos_hint={'center_y': 0.65, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.food.add_widget(food_label)
        home_food_labels.append(food_label)

        notes = user.get_food_score()[1]
        third_recommendation_label = MDLabel(
            text="-Recommendation Note: " + notes[0],
            pos_hint={'center_y': 0.20, 'center_x': 0.4},
            halign="center",
            markup=True,
            bold=False,
            size=(0.2, 0.075)
        )
        self.food.add_widget(third_recommendation_label)
        home_food_labels.append(third_recommendation_label)

    def exercise_enter(self):
        global home_exercise_labels
        global exercise
        for i in range(len(home_exercise_labels)):
            self.exercise.remove_widget(home_exercise_labels[i])

        exercise.update_score()
        ex_score = exercise.get_score()
        intex_score = int(ex_score)
        exercise_label = MDLabel(
            text=str(intex_score),
            pos_hint={'center_y': 0.65, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.exercise.add_widget(exercise_label)
        home_exercise_labels.append(exercise_label)

        first_recommendation_label = MDLabel(
            text=user.get_name() + "\'s workout" + " recommendation for today is: ",
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=False,
            font_style="H5"
        )
        self.exercise.add_widget(first_recommendation_label)
        home_exercise_labels.append(first_recommendation_label)

        recommendation = user.get_exercise_recommendation()
        second_recommendation_label = MDLabel(
            text="*" + recommendation + "*",
            pos_hint={'center_y': 0.35, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H5"
        )
        self.exercise.add_widget(second_recommendation_label)
        home_exercise_labels.append(second_recommendation_label)

        steps = exercise.get_steps()
        third_recommendation_label = MDLabel(
            text="-Steps taken today: " + str(steps),
            pos_hint={'center_y': 0.20, 'center_x': 0.3},
            halign="center",
            markup=True,
            bold=False,
            size=(0.2, 0.075)
        )
        self.exercise.add_widget(third_recommendation_label)
        home_exercise_labels.append(third_recommendation_label)

    def sleep_enter(self):
        global home_sleep_labels
        global user
        for i in range(len(home_sleep_labels)):
            self.sleep.remove_widget(home_sleep_labels[i])

        sleep_score = user.get_sleep_score()
        sleep_label = MDLabel(
            text=str(sleep_score),
            pos_hint={'center_y': 0.65, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H3"
        )
        self.sleep.add_widget(sleep_label)
        home_sleep_labels.append(sleep_label)

        first_recommendation_label = MDLabel(
            text=user.get_name() + "\'s sleep" + " recommendation for tonight is to go to bed at: ",
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=False,
            font_style="H5"
        )
        self.sleep.add_widget(first_recommendation_label)
        home_sleep_labels.append(first_recommendation_label)

        recommendation = user.get_sleep_recommendation()
        second_recommendation_label = MDLabel(
            text="*" + recommendation + "PM" + "*",
            pos_hint={'center_y': 0.35, 'center_x': 0.5},
            halign="center",
            markup=True,
            bold=True,
            font_style="H5"
        )
        self.sleep.add_widget(second_recommendation_label)
        home_sleep_labels.append(second_recommendation_label)

        notes = user.get_sleep_notes()
        third_recommendation_label = MDLabel(
            text="-Recommendation Note: " + notes,
            pos_hint={'center_y': 0.20, 'center_x': 0.42},
            halign="center",
            markup=True,
            bold=False,
            size=(0.2, 0.075)
        )
        self.sleep.add_widget(third_recommendation_label)
        home_sleep_labels.append(third_recommendation_label)


food_labels = []
food_buttons = []
food_done_button = None
selected_food = ""


class FoodScreen(Screen):
    def food_back(self):
        global food_labels
        global food_buttons
        global food_done_button

        for i in range(len(food_labels)):
            self.remove_widget(food_labels[i])
            self.remove_widget(food_buttons[i])

        if food_done_button is not None:
            self.remove_widget(food_done_button)

        self.parent.current = "home"

    def food_enter(self):
        global user
        global food
        global food_labels
        global food_buttons
        global food_done_button

        for i in range(len(food_labels)):
            self.remove_widget(food_labels[i])
            self.remove_widget(food_buttons[i])

        self.results = food.search_food(self.meal.text)

        size = min(len(self.results), 5)
        for i in range(size):
            label = MDLabel(
                text=self.results[i].description,
                pos_hint={'center_x': 0.5, 'center_y': 0.65 - (0.1 * i)},
                halign="center",
                markup=True,
                bold=False,
                size=(0.2, 0.075)
            )
            if i == 0:
                button = MDCheckbox(
                    group="food",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_food_result(0, *args)
                )
            elif i == 1:
                button = MDCheckbox(
                    group="food",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_food_result(1, *args)
                )
            elif i == 2:
                button = MDCheckbox(
                    group="food",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_food_result(2, *args)
                )
            elif i == 3:
                button = MDCheckbox(
                    group="food",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_food_result(3, *args)
                )
            elif i == 4:
                button = MDCheckbox(
                    group="food",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_food_result(4, *args)
                )
            self.add_widget(label)
            self.add_widget(button)
            food_labels.append(label)
            food_buttons.append(button)

        done_button = MDRoundFlatButton(
            text="Confirm",
            size_hint=(None, None),
            size=(110, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            on_press=self.food_confirm
        )

        self.add_widget(done_button)
        food_done_button = done_button

    def toggle_food_result(self, index, t):
        global selected_food
        selected_food = self.results[index]

    def food_confirm(self, t):
        global food_labels
        global food_buttons
        global food_done_button

        for i in range(len(food_labels)):
            self.remove_widget(food_labels[i])
            self.remove_widget(food_buttons[i])
        self.remove_widget(food_done_button)

        self.parent.current = "final_food"


class FinalFoodScreen(Screen):
    def toggle_yes(self):
        self.like = "yes"

    def toggle_soso(self):
        self.like = "soso"

    def toggle_no(self):
        self.like = "no"

    def toggle_am(self):
        self.ampm = "am"

    def toggle_pm(self):
        self.ampm = "pm"

    def toggle_breakfast(self):
        self.type = "Breakfast"

    def toggle_lunch(self):
        self.type = "Lunch"

    def toggle_dinner(self):
        self.type = "Dinner"

    def toggle_snack(self):
        self.type = "Snack"

    def now_time(self):
        dt = datetime.datetime.now()
        self.month.text = str(dt.month)
        self.day.text = str(dt.day)
        self.year.text = str(dt.year)
        self.minute.text = str(dt.minute)

        if dt.hour >= 13:
            self.hour.text = str(dt.hour - 12)
            self.pm.active = True
            self.am.active = False
            self.ampm = "pm"
        elif dt.hour == 12:
            self.hour.text = str(dt.hour)
            self.am.active = False
            self.pm.active = True
            self.ampm = "pm"
        else:
            self.hour.text = str(dt.hour)
            self.am.active = True
            self.pm.active = False
            self.ampm = "am"

    def final_food_enter(self):
        global food
        global selected_food
        global user

        self.hourint = int(self.hour.text)
        if (self.ampm == "pm"):
            self.hourint += 12
        dt = datetime.datetime(int(self.year.text), int(self.month.text), int(self.day.text), self.hourint,
                               int(self.minute.text))

        lk = -1
        if self.like == "yes":
            lk = 1
        elif self.like == "no":
            lk = 2
        elif self.like == "soso":
            lk = 0

        food.input_food_log(selected_food.fdc_id, dt, self.type, lk)

        self.pm.active = False
        self.am.active = False
        self.yes.active = False
        self.soso.active = False
        self.no.active = False
        self.breakfast.active = False
        self.lunch.active = False
        self.dinner.active = False
        self.snack.active = False
        self.year.text = ""
        self.month.text = ""
        self.day.text = ""
        self.hour.text = ""
        self.minute.text = ""

        self.parent.current = "home"

        self.food_type = "Snack"
        dt = datetime.datetime.now()
        if dt.hour <= 10:
            self.food_type = "Breakfast"
        elif dt.hour <= 16:
            self.food_type = "Lunch"
        else:
            self.food_type = "Dinner"
        user.set_food_recommendation(food.recommend(self.food_type))

        user.set_food_score(food.grade())


exercise_labels = []
exercise_buttons = []
exercise_done_button = None
selected_exercise = ""


class ExerciseScreen(Screen):
    def exercise_back(self):
        global exercise_labels
        global exercise_buttons
        global exercise_done_button

        for i in range(len(exercise_labels)):
            self.remove_widget(exercise_labels[i])
            self.remove_widget(exercise_buttons[i])

        if exercise_done_button is not None:
            self.remove_widget(exercise_done_button)

        self.parent.current = "home"

    def exercise_enter(self):
        global user
        global exercise2
        global exercise_labels
        global exercise_buttons
        global exercise_done_button

        for i in range(len(exercise_labels)):
            self.remove_widget(exercise_labels[i])
            self.remove_widget(exercise_buttons[i])

        self.results = exercise2.search_exercise(self.workout.text)

        size = min(len(self.results), 5)
        for i in range(size):
            label = MDLabel(
                text=self.results[i].get_name(),
                pos_hint={'center_x': 0.5, 'center_y': 0.65 - (0.1 * i)},
                halign="center",
                markup=True,
                bold=False,
                size=(0.2, 0.075)
            )
            if i == 0:
                button = MDCheckbox(
                    group="exercise",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_exercise_result(0, *args)
                )
            elif i == 1:
                button = MDCheckbox(
                    group="exercise",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_exercise_result(1, *args)
                )
            elif i == 2:
                button = MDCheckbox(
                    group="exercise",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_exercise_result(2, *args)
                )
            elif i == 3:
                button = MDCheckbox(
                    group="exercise",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_exercise_result(3, *args)
                )
            elif i == 4:
                button = MDCheckbox(
                    group="exercise",
                    pos_hint={'center_x': 0.05, 'center_y': 0.65 - (0.1 * i)},
                    size_hint=(None, None),
                    size=(70, 70),
                    on_press=lambda *args: self.toggle_exercise_result(4, *args)
                )
            self.add_widget(label)
            self.add_widget(button)
            exercise_labels.append(label)
            exercise_buttons.append(button)

        done_button = MDRoundFlatButton(
            text="Confirm",
            size_hint=(None, None),
            size=(110, 35),
            pos_hint={'center_x': 0.5, 'center_y': 0.05},
            on_press=self.exercise_confirm
        )

        self.add_widget(done_button)
        exercise_done_button = done_button

    def toggle_exercise_result(self, index, t):
        global selected_exercise
        global exercise
        self.selected_exercise = self.results[index]

    def exercise_confirm(self, t):
        global user
        global exercise_labels
        global exercise_labels
        global exercise_done_button

        for i in range(len(exercise_labels)):
            self.remove_widget(exercise_labels[i])
            self.remove_widget(exercise_buttons[i])
        self.remove_widget(exercise_done_button)

        self.parent.current = "home"

        exercise.add_exercise(self.selected_exercise)
        user.set_exercise_recommendation(exercise.get_exercise_recommendation())


class SleepScreen(Screen):
    def toggle_sleep_am(self):
        self.sleep_ampm = "am"

    def toggle_sleep_pm(self):
        self.sleep_ampm = "pm"

    def toggle_wakeup_am(self):
        self.wakeup_ampm = "am"

    def toggle_wakeup_pm(self):
        self.wakeup_ampm = "pm"

    def toggle_well(self):
        self.like = "well"

    def toggle_soso(self):
        self.like = "soso"

    def toggle_bad(self):
        self.bad = "bad"

    def now_time(self):
        dt = datetime.datetime.now()
        self.wakeup_minute.text = str(dt.minute)

        if dt.hour >= 13:
            self.wakeup_hour.text = str(dt.hour - 12)
            self.wakeup_pm.active = True
            self.wakeup_am.active = False
            self.wakeup_ampm = "pm"
        elif dt.hour == 12:
            self.wakeup_hour.text = str(dt.hour)
            self.wakeup_pm.active = True
            self.wakeup_am.active = False
            self.wakeup_ampm = "pm"
        else:
            self.wakeup_hour.text = str(dt.hour)
            self.wakeup_am.active = True
            self.wakeup_pm.active = False
            self.wakeup_ampm = "am"

    def sleep_back(self):
        self.sleep_pm.active = False
        self.sleep_am.active = False
        self.wakeup_pm.active = False
        self.wakeup_am.active = False
        self.well.active = False
        self.soso.active = False
        self.bad.active = False
        self.sleep_hour.text = ""
        self.sleep_minute.text = ""
        self.wakeup_hour.text = ""
        self.wakeup_minute.text = ""

        self.parent.current = "home"

    def sleep_enter(self):
        today = datetime.datetime.now()
        if int(self.sleep_hour.text) >= 7:
            self.sleep_day = today - datetime.timedelta(1)
        else:
            self.sleep_day = today

        global user

        self.sleep_hourint = int(self.sleep_hour.text)
        if (self.sleep_ampm == "pm"):
            self.sleep_hourint += 12
        sleep_dt = datetime.datetime(self.sleep_day.year, self.sleep_day.month, self.sleep_day.day, self.sleep_hourint,
                                     int(self.sleep_minute.text))

        self.wakeup_hourint = int(self.wakeup_hour.text)
        if (self.wakeup_ampm == "pm"):
            self.wakeup_hourint += 12
        wakeup_dt = datetime.datetime(today.year, today.month, today.day, self.wakeup_hourint,
                                      int(self.wakeup_minute.text))

        slp = Sleep(sleep_dt, wakeup_dt, self.like)
        user.enter_sleep(slp)

        self.sleep_pm.active = False
        self.sleep_am.active = False
        self.wakeup_pm.active = False
        self.wakeup_am.active = False
        self.well.active = False
        self.soso.active = False
        self.bad.active = False
        self.sleep_hour.text = ""
        self.sleep_minute.text = ""
        self.wakeup_hour.text = ""
        self.wakeup_minute.text = ""

        self.parent.current = "home"


class Main(MDApp):
    def build(self):
        return Manager()


if __name__ == '__main__':
    Main().run()

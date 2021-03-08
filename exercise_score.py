import random

class ExerciseScore:

    def __init__(self, per_week, height, weight, goals):
        self.prev_week = [0]*7
        for i in range(per_week):               # list of length 7, storing whether user has exercised for past 7 days.
            self.prev_week[i] = 1
        self.score = 0                          # out of 10
        self.weight = weight                    # weight in kgs
        self.height = height                    # height in cms
        self.muscles = ['Calisthenics', 'Biceps workout', 'Chest workout', 'Triceps workout', 'Leg workout', 'Back workout', 'Ab workout', 'Shoulder workout']
        self.cardio = ['Cycling','Aerobics','Yoga', 'Dance','Running', 'Sports', 'Walking', 'Swimming']
        self.goals = set(goals)                      # set containing goals that user selected
        self.update_score()
        self.days_last_workout = 0
        self.last_exercise = None
        
        
    def bmi_score(self):                        # out of 5
        metres = self.height/100
        bmi = self.weight/(metres**2)
        if bmi >= 18.5 and bmi <= 24.5:
            return 5
        else:
            if bmi >= 16.5 and bmi <= 18.5:
                return 3
            elif bmi < 16.5:
                return 2
            elif bmi > 24.5 and bmi <= 30:
                return 3
            elif bmi > 30:
                return 1

    def activity_score(self):                   # out of 5
        return (sum(self.prev_week)/7) * 5


    def update_weight(self, w):                 # update weight of user
        self.weight = w
        self.update_score()

    def update_height(self, h):                 # update height of user
        self.height = h
        self.update_score()
        
    def update_score(self):
        self.score = self.bmi_score() + self.activity_score()
        
    
    def add_exercise(self, exercise):           # user prompted daily to see if they exercised that day.
        self.last_exercise = exercise           # exercise parameter is the exercise_category from exercise.py, or None if not exercised.
        self.prev_week.pop(0)
        if exercise:
            self.prev_week.append(1)
            self.days_last_workout = 0
        else:
            self.prev_week.append(0)
            self.days_last_workout += 1
        self.update_score()

    def get_exercise_recommendation(self):
        exercises = []
        if 'Gain Muscle' in self.goals:
            exercises.extend(self.muscles)          # if goal is to gain muscle, add muscle workouts to possible recommendations 
        if 'Lose Weight' in self.goals:
            exercises.extend(self.cardio)           # if goal is to lose weight, add cardio workouts to possible recommendations
        if len(exercises) == 0:
            exercises.extend(self.muscles)          # if no goals, select from all exercises
            exercises.extend(self.cardio)
        if self.last_exercise in exercises:
            exercises.remove(self.last_exercise)    # remove last_exercise so it is not recommended again
        return random.choice(exercises)
        
    def get_steps(self):
        return random.randrange(500,10000)

    def get_score(self):
        return self.score

    def get_days_since_last_workout(self):
        return self.days_last_workout

    
            


##h = 170
##w = 300
##per_week = 6
##goals = ['Gain Muscle']
##user = ExerciseScore(per_week,h,w,goals)
##print(user.score)
##user.add_exercise(0)
##print(user.score)
##user.add_exercise(0)
##print(user.score)
##user.add_exercise(1)
##user.add_exercise(1)
##user.add_exercise(1)
##print(user.score)
##user.add_exercise(1)
##user.add_exercise(1)
##user.add_exercise(1)
##user.add_exercise(1)
##user.add_exercise(1)
##print(user.score)
##user.update_weight(75)
##print(user.score)
##user.update_height(175)
##print(user.score)
##print(user.get_exercise_recommendation())
##user.add_exercise('Cycling')
##print(user.get_days_since_last_workout())
##user.add_exercise(None)
##print(user.get_days_since_last_workout())
##user.add_exercise(None)
##print(user.get_days_since_last_workout())
##user.add_exercise(None)
##print(user.get_days_since_last_workout())
##
##user.add_exercise(None)
##print(user.get_days_since_last_workout())
##
##print(user.get_exercise_recommendation())
##user.add_exercise('Swimming')
##print(user.get_exercise_recommendation())
##user.add_exercise('Back workout')
##print(user.get_exercise_recommendation())
##print(user.get_days_since_last_workout())
##print(user.get_steps())




        
        


    

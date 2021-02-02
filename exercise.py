from pathlib import Path
import csv
from collections import defaultdict, deque

SCRIPT_LOCATION = Path(__file__).absolute().parent
DB_LOCATION = SCRIPT_LOCATION / "db"
DB_EXERCISE_LOCATION = DB_LOCATION / "exercise_dataset.csv"

EXERCISE_CATEGORIES = {
    0: "Cycling",
    1: "Calisthenics",
    2: "Weight Training",
    3: "Exercise Machines",
    4: "Aerobics",
    5: "Yoga",
    6: "Dance",
    7: "Running",
    8: "Sports",
    9: "Walking",
    10: "Swimming",
    11: "Miscellaneous"
}

class Exercise:
    def __init__(self, id, name, calories):
        self.id = id
        self.name = name
        self.categoryId = self.set_category()
        self.category = EXERCISE_CATEGORIES[self.categoryId]

    def set_category(self):
        '''Gives exercise a category from id based on csv file'''
        if self.id <= 12:
            return 0
        if self.id <= 14:
            return 1
        if self.id <= 17:
            return 2
        if self.id <= 24:
            return 3
        if self.id <= 28 or self.id == 32 or self.id == 33:
            return 4
        if self.id == 31 or self.id == 30:
            return 5
        if self.id <= 36:
            return 6
        if self.id <= 51:
            return 7
        if self.id <= 140:
            return 8
        if self.id == 141 or (151 <= self.id <= 174):
            return 9
        if self.id <= 193:
            return 8
        if self.id <= 208:
            return 10
        if self.id <= 223:
            return 8
        return 11

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    '''def get_calories(self):
        return self.calories'''


class ExerciseDatabase:
    def __init__(self):
        self.exercises = defaultdict(Exercise)
        self.load_exercises()

    def load_exercises(self):
        with open(DB_EXERCISE_LOCATION, 'r', newline='') as csvfile:
            csvfile.readline()

            for id, row in enumerate(csv.reader(csvfile)):
                exer = Exercise(id, row[0], row[-1])
#               self.get_calories(exer, weight, KGcalories)
                self.exercises[id] = exer

    '''def get_calories(self, exercise, weight, cals):
        #Gets Calories based on user weight
        CONVERSION_CONSTANT = 0.453592
        KGweight = weight*CONVERSION_CONSTANT
        calroies = cals*KGweight
        return calories
    '''

    def search_exercise(self, name):
        return [exercise for exercise in self.exercises.values() if name.lower() in
                exercise.get_name().lower()]

db = ExerciseDatabase()
print("Search results for running:")
for exercise in db.search_exercise("running"):
    print(exercise.get_name())
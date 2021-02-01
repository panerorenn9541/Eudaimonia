from typing import *
import os
from pathlib import Path
import csv

SCRIPT_LOCATION = Path(__file__).absolute().parent
DB_LOCATION = SCRIPT_LOCATION / "db"
DB_CATEGORY_LOCATION = DB_LOCATION / "wweia_food_category.csv"
DB_FOOD_LOCATION = DB_LOCATION / "food_reduced.csv"
DB_NUTRIENT_LOCATION = DB_LOCATION / "nutrient.csv"
DB_FOOD_NUTRIENT_LOCATION = DB_LOCATION / "food_nutrient.csv"


class FoodCategory(NamedTuple):
    id_: int
    description: str


class NutrientCategory(NamedTuple):
    id_: int
    name: str
    unit: str


class Nutrient(NamedTuple):
    nutrient_category: NutrientCategory
    amount: float


class Food(NamedTuple):
    fdc_id: int
    description: str
    food_category: FoodCategory
    nutrients: List[Nutrient]


class FoodDatabase:
    food_categories: Dict[int, FoodCategory]
    nutrient_categories: Dict[int, NutrientCategory]
    foods = Dict[int, Food]


    def __init__(self) -> None:
        self.food_categories = {}
        self.nutrient_categories = {}
        self.foods = {}

        self.load_food_categories()
        self.load_nutrient_categories()
        self.load_foods()
        self.load_food_nutrients()


    def load_food_categories(self) -> None:
        with open(DB_CATEGORY_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for id_, description in csv.reader(csvfile):
                id_ = int(id_)
                self.food_categories[id_] = FoodCategory(id_, description)


    def load_nutrient_categories(self) -> None:
        with open(DB_NUTRIENT_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for id_, name, unit, _, _ in csv.reader(csvfile):
                id_ = int(id_)
                self.nutrient_categories[id_] = NutrientCategory(id_, name,
                                                                 unit)


    def load_foods(self) -> None:
        with open(DB_FOOD_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            #csvfile.readline()

            for fdc_id, _, description, food_category_id, _ in csv.reader(csvfile):
                fdc_id = int(fdc_id)
                food_category_id = int(food_category_id)
                if food_category_id:
                    self.foods[fdc_id] = \
                        Food(fdc_id, description,
                             self.food_categories[food_category_id], [])


    def load_food_nutrients(self) -> None:
        with open(DB_FOOD_NUTRIENT_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for _, fdc_id, nutrient_id, amount, *_ in csv.reader(csvfile):
                fdc_id = int(fdc_id)
                nutrient_id = int(nutrient_id)
                amount = float(amount)
                #self.foods[fdc_id].nutrients.append(self.nutrient_categories[nutrient_id])
                self.foods[fdc_id].nutrients.append(
                    Nutrient(self.nutrient_categories[nutrient_id], amount))


    def search_food(self, name: str) -> List[Food]:
        # Super simple food search, probably the reason why we are in a class
        # named next-gen search systems
        #
        # Once we port this over to an actual database, this will be more robust
        return [food for food in self.foods.values() if name.lower() in
                food.description.lower()]

a = FoodDatabase()
print("Search results for Clam Chowder:")
for food in a.search_food("Clam Chowder"):
    print(food.description)

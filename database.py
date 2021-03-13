from typing import *
from dataclasses import dataclass
from sqlite3 import connect, Connection
import os
from pathlib import Path
import csv
import datetime
from collections import defaultdict
from itertools import zip_longest

SCRIPT_LOCATION = Path(__file__).absolute().parent
DB_LOCATION = SCRIPT_LOCATION / "db"
DB_CATEGORY_LOCATION = DB_LOCATION / "wweia_food_category.csv"
DB_FOOD_LOCATION = DB_LOCATION / "food_reduced.csv"
DB_NUTRIENT_LOCATION = DB_LOCATION / "nutrient.csv"
DB_FOOD_NUTRIENT_LOCATION = DB_LOCATION / "food_nutrient.csv"

FoodType = Literal["Breakfast", "Lunch", "Dinner", "Snack"]
PersonStatus = Literal["Male", "Female", "Pregnant", "Lactating"]

class FoodCategory(NamedTuple):
    id_: int
    description: str


class NutrientCategory(NamedTuple):
    id_: int
    name: str
    unit: str


class Nutrient(NamedTuple):
    nutrient_category_id: int
    amount: float


class Food(NamedTuple):
    fdc_id: int
    description: str
    food_category_id: int

class Database:
    conn: Connection
    target_daily: List[Tuple[int, float]]
    friendly_nutrient_names: Dict[int, str]

    def __del__(self):
        # Make sure we commit before we destroy our connection!
        # Data loss occurs here if __del__ isn't called!
        self.conn.commit()

    def __init__(self, location="temp.db", age: int = 19,
                 status: PersonStatus = "Male") -> None:
        self.conn = connect(location)
        self.migrate()


        # People younger than 8 years old and older than 999 years old are
        # assumed not to use our app
        #
        # Assume women won't be pregnant/lactate before 14 years old and after
        # 50 years
        #
        # Other is the Daily Value recommendation by the FDA, the specific info is
        # the values recommended by the NIH
        #
        # https://ods.od.nih.gov/HealthInformation/Dietary_Reference_Intakes.aspx
        # (specifically the first three tables under "DRI Tables")
        #
        # https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels
        #
        # I only used nutrients that probably have a greater impact on your
        # health. For example, I never had to worry about Selenium consumption
        #
        # energy            Energy                              1008    KCAL
        # carbohydrate      Carbohydrate, by difference         1005    G
        # fiber             Fiber, total dietary                1079    G
        # fat               Total lipid (fat)                   1004    G
        # protein           Protein                             1003    G
        # vitamina          Vitamin A, RAE                      1106    UG
        # vitaminc          Vitamin C, total ascorbic acid      1162    MG
        # vitamind          Vitamin D (D2 + D3)                 1114    UG
        # vitamine          Vitamin E (alpha-tocopherol)        1109    MG
        # vitaminb6         Vitamin B-6                         1175    MG
        # vitaminb12        Vitamin B-12                        1178    UG
        # calcium           Calcium, Ca                         1087    MG
        # iron              Iron, Fe                            1089    MG
        # sodium            Sodium, Na                          1093    MG

        self.friendly_nutrient_names = {
            1008: "Calorie",
            1005: "Carbohydrate",
            1079: "Fiber",
            1004: "Fat",
            1003: "Protein",
            1106: "Vitamin A",
            1162: "Vitamin C",
            1114: "Vitamin D",
            1109: "Vitamin E",
            1175: "Vitamin B6",
            1178: "Vitamin B12",
            1087: "Calcium",
            1089: "Iron",
            1093: "Sodium"
        }

        #table = {
        #    "Male": [
        #        [9, 13, (130, 31, 34, 600, 45, 15, 11, 1, 1.8, 1300, 8, 1200)],
        #        [14, 18, (130, 38, 52, 900, 75, 15, 15, 1.3, 2.4, 1300, 11, 1500)],
        #        [19, 30, (130, 38, 56, 900, 90, 15, 15, 1.3, 2.4, 1000, 8, 1500)],
        #        [31, 50, (130, 38, 56, 900, 90, 15, 15, 1.3, 2.4, 1000, 8, 1500)],
        #        [51, 70, (130, 30, 56, 900, 90, 15, 15, 1.7, 2.4, 1000, 8, 1500)],
        #        [71, 999, (130, 30, 56, 900, 90, 20, 15, 1.7, 2.4, 1200, 8, 1500)]
        #    ], "Female": [
        #        [9, 13, (130, 26, 34, 600, 45, 15, 11, 1, 1.8, 1300, 8, 1200)],
        #        [14, 18, (130, 26, 46, 700, 65, 15, 15, 1.2, 2.4, 1300, 15, 1500)],
        #        [19, 30, (130, 25, 46, 701, 75, 15, 15, 1.3, 2.4, 1000, 18, 1500)],
        #        [31, 50, (130, 25, 46, 702, 75, 15, 15, 1.3, 2.4, 1000, 18, 1500)],
        #        [51, 70, (130, 21, 46, 703, 75, 15, 15, 1.5, 2.4, 1200, 8, 1500)],
        #        [71, 999, (130, 21, 46, 704, 75, 20, 15, 1.5, 2.4, 1200, 8, 1500)]
        #    ], "Pregnant": [
        #        [14, 18, (175, 28, 71, 750, 80, 15, 15, 1.9, 2.6, 1300, 27, 1500)],
        #        [19, 30, (175, 28, 71, 770, 85, 15, 15, 1.9, 2.6, 1000, 27, 1500)],
        #        [31, 50, (175, 28, 71, 770, 85, 15, 15, 1.9, 2.6, 1000, 27, 1500)]
        #    ], "Lactation": [
        #        [14, 18, (210, 29, 71, 1200, 115, 15, 19, 2, 2.8, 1300, 10, 1500)],
        #        [19, 30, (210, 29, 71, 1300, 120, 15, 19, 2, 2.8, 1000, 9, 1500)],
        #        [31, 50, (210, 29, 71, 1300, 120, 15, 19, 2, 2.8, 1000, 9, 1500)]
        #    ]
        #}

        #table = {
        #    "Male": [
        #        [9, 13,   (2000, 78, 130, 31, 34, 600, 45, 15, 11, 1, 1.8, 1300, 8, 1200)],
        #        [14, 18,  (2000, 78, 130, 38, 52, 900, 75, 15, 15, 1.3, 2.4, 1300, 11, 1500)],
        #        [19, 30,  (2000, 78, 130, 38, 56, 900, 90, 15, 15, 1.3, 2.4, 1000, 8, 1500)],
        #        [31, 50,  (2000, 78, 130, 38, 56, 900, 90, 15, 15, 1.3, 2.4, 1000, 8, 1500)],
        #        [51, 70,  (2000, 78, 130, 30, 56, 900, 90, 15, 15, 1.7, 2.4, 1000, 8, 1500)],
        #        [71, 999, (2000, 78, 130, 30, 56, 900, 90, 20, 15, 1.7, 2.4, 1200, 8, 1500)]
        #    ], "Female": [
        #        [9, 13,   (2000, 78, 130, 26, 34, 600, 45, 15, 11, 1, 1.8, 1300, 8, 1200)],
        #        [14, 18,  (2000, 78, 130, 26, 46, 700, 65, 15, 15, 1.2, 2.4, 1300, 15, 1500)],
        #        [19, 30,  (2000, 78, 130, 25, 46, 701, 75, 15, 15, 1.3, 2.4, 1000, 18, 1500)],
        #        [31, 50,  (2000, 78, 130, 25, 46, 702, 75, 15, 15, 1.3, 2.4, 1000, 18, 1500)],
        #        [51, 70,  (2000, 78, 130, 21, 46, 703, 75, 15, 15, 1.5, 2.4, 1200, 8, 1500)],
        #        [71, 999, (2000, 78, 130, 21, 46, 704, 75, 20, 15, 1.5, 2.4, 1200, 8, 1500)]
        #    ], "Pregnant": [
        #        [14, 18,  (2000, 78, 175, 28, 71, 750, 80, 15, 15, 1.9, 2.6, 1300, 27, 1500)],
        #        [19, 30,  (2000, 78, 175, 28, 71, 770, 85, 15, 15, 1.9, 2.6, 1000, 27, 1500)],
        #        [31, 50,  (2000, 78, 175, 28, 71, 770, 85, 15, 15, 1.9, 2.6, 1000, 27, 1500)]
        #    ], "Lactation": [
        #        [14, 18,  (2000, 78, 210, 29, 71, 1200, 115, 15, 19, 2, 2.8, 1300, 10, 1500)],
        #        [19, 30,  (2000, 78, 210, 29, 71, 1300, 120, 15, 19, 2, 2.8, 1000, 9, 1500)],
        #        [31, 50,  (2000, 78, 210, 29, 71, 1300, 120, 15, 19, 2, 2.8, 1000, 9, 1500)]
        #    ]
        #}
        #other = [2000, 78, 275, 78, 50, 900, 90, 20, 15, 1.7, 2.4, 1300, 18, 2300]
        #ids = [1008, 1004, 1005, 1079, 1003, 1106, 1162, 1114, 1109, 1175, 1178, 1087, 1089, 1093]
        #print(dict(zip(ids,other)))
        #print({___: [[min_, max_, {ids[i]: _ for i, _ in enumerate(x)}] for min_, max_, x in __] for ___, __ in table.items()})

        table2 = {'Male': [
            [9, 13, {1008: 2000, 1004: 78, 1005: 130, 1079: 31, 1003: 34, 1106: 600, 1162: 45, 1114: 15, 1109: 11, 1175: 1, 1178: 1.8, 1087: 1300, 1089: 8, 1093: 1200}],
            [14, 18, {1008: 2000, 1004: 78, 1005: 130, 1079: 38, 1003: 52, 1106: 900, 1162: 75, 1114: 15, 1109: 15, 1175: 1.3, 1178: 2.4, 1087: 1300, 1089: 11, 1093: 1500}],
            [19, 30, {1008: 2000, 1004: 78, 1005: 130, 1079: 38, 1003: 56, 1106: 900, 1162: 90, 1114: 15, 1109: 15, 1175: 1.3, 1178: 2.4, 1087: 1000, 1089: 8, 1093: 1500}],
            [31, 50, {1008: 2000, 1004: 78, 1005: 130, 1079: 38, 1003: 56, 1106: 900, 1162: 90, 1114: 15, 1109: 15, 1175: 1.3, 1178: 2.4, 1087: 1000, 1089: 8, 1093: 1500}],
            [51, 70, {1008: 2000, 1004: 78, 1005: 130, 1079: 30, 1003: 56, 1106: 900, 1162: 90, 1114: 15, 1109: 15, 1175: 1.7, 1178: 2.4, 1087: 1000, 1089: 8, 1093: 1500}],
            [71, 999, {1008: 2000, 1004: 78, 1005: 130, 1079: 30, 1003: 56, 1106: 900, 1162: 90, 1114: 20, 1109: 15, 1175: 1.7, 1178: 2.4, 1087: 1200, 1089: 8, 1093: 1500}]
        ],'Female': [
            [9, 13, {1008: 2000, 1004: 78, 1005: 130, 1079: 26, 1003: 34, 1106: 600, 1162: 45, 1114: 15, 1109: 11, 1175: 1, 1178: 1.8, 1087: 1300, 1089: 8, 1093: 1200}],
            [14, 18, {1008: 2000, 1004: 78, 1005: 130, 1079: 26, 1003: 46, 1106: 700, 1162: 65, 1114: 15, 1109: 15, 1175: 1.2, 1178: 2.4, 1087: 1300, 1089: 15, 1093: 1500}],
            [19, 30, {1008: 2000, 1004: 78, 1005: 130, 1079: 25, 1003: 46, 1106: 701, 1162: 75, 1114: 15, 1109: 15, 1175: 1.3, 1178: 2.4, 1087: 1000, 1089: 18, 1093: 1500}],
            [31, 50, {1008: 2000, 1004: 78, 1005: 130, 1079: 25, 1003: 46, 1106: 702, 1162: 75, 1114: 15, 1109: 15, 1175: 1.3, 1178: 2.4, 1087: 1000, 1089: 18, 1093: 1500}],
            [51, 70, {1008: 2000, 1004: 78, 1005: 130, 1079: 21, 1003: 46, 1106: 703, 1162: 75, 1114: 15, 1109: 15, 1175: 1.5, 1178: 2.4, 1087: 1200, 1089: 8, 1093: 1500}],
            [71, 999, {1008: 2000, 1004: 78, 1005: 130, 1079: 21, 1003: 46, 1106: 704, 1162: 75, 1114: 20, 1109: 15, 1175: 1.5, 1178: 2.4, 1087: 1200, 1089: 8, 1093: 1500}]
        ], 'Pregnant': [
            [14, 18, {1008: 2000, 1004: 78, 1005: 175, 1079: 28, 1003: 71, 1106: 750, 1162: 80, 1114: 15, 1109: 15, 1175: 1.9, 1178: 2.6, 1087: 1300, 1089: 27, 1093: 1500}],
            [19, 30, {1008: 2000, 1004: 78, 1005: 175, 1079: 28, 1003: 71, 1106: 770, 1162: 85, 1114: 15, 1109: 15, 1175: 1.9, 1178: 2.6, 1087: 1000, 1089: 27, 1093: 1500}],
            [31, 50, {1008: 2000, 1004: 78, 1005: 175, 1079: 28, 1003: 71, 1106: 770, 1162: 85, 1114: 15, 1109: 15, 1175: 1.9, 1178: 2.6, 1087: 1000, 1089: 27, 1093: 1500}]
        ], 'Lactation': [
            [14, 18, {1008: 2000, 1004: 78, 1005: 210, 1079: 29, 1003: 71, 1106: 1200, 1162: 115, 1114: 15, 1109: 19, 1175: 2, 1178: 2.8, 1087: 1300, 1089: 10, 1093: 1500}],
            [19, 30, {1008: 2000, 1004: 78, 1005: 210, 1079: 29, 1003: 71, 1106: 1300, 1162: 120, 1114: 15, 1109: 19, 1175: 2, 1178: 2.8, 1087: 1000, 1089: 9, 1093: 1500}],
            [31, 50, {1008: 2000, 1004: 78, 1005: 210, 1079: 29, 1003: 71, 1106: 1300, 1162: 120, 1114: 15, 1109: 19, 1175: 2, 1178: 2.8, 1087: 1000, 1089: 9, 1093: 1500}]]}

        other = {1008: 2000, 1004: 78, 1005: 275, 1079: 78, 1003: 50, 1106: 900, 1162: 90, 1114: 20, 1109: 15, 1175: 1.7, 1178: 2.4, 1087: 1300, 1089: 18, 1093: 2300}

        for row in table2[status]:
            if row[0] <= age <= row[1]:
                self.target_daily = row[2]
                break
        else:
            self.target_daily = row[2]


    #####
    #
    # Migration
    #
    #####

    def migrate(self) -> None:
        c = self.conn.cursor()
        c.execute("""PRAGMA foreign_keys = ON;""")

        # Create the tables
        c.executescript("""
        DROP TABLE IF EXISTS food_log;
        DROP TABLE IF EXISTS food_exclusion;
        DROP TABLE IF EXISTS curated_foods;
        DROP TABLE IF EXISTS prioritized_nutrients;
        """)
        c.executescript("""
        CREATE TABLE IF NOT EXISTS food_categories(
            id INTEGER PRIMARY KEY,
            descr TEXT
        );

        CREATE TABLE IF NOT EXISTS nutrient_categories(
            id INTEGER PRIMARY KEY,
            name TEXT,
            unit TEXT
        );

        CREATE TABLE IF NOT EXISTS foods(
            id INTEGER PRIMARY KEY,
            descr TEXT,
            food_category_id INTEGER REFERENCES food_categories(id),
            liked INTEGER
        );

        CREATE TABLE IF NOT EXISTS food_nutrients_junction(
            id INTEGER PRIMARY KEY,
            food_id INTEGER REFERENCES foods(id),
            nutrient_id INTEGER REFERENCES nutrient_categories(id),
            amount REAL
        );

        CREATE TABLE IF NOT EXISTS food_log(
            id INTEGER PRIMARY KEY,
            food_id INTEGER REFERENCES foods(id),
            datetim TEXT,
            type TEXT
        );

        CREATE TABLE IF NOT EXISTS food_exclusion(
            id INTEGER PRIMARY KEY,
            food_category_id INTEGER REFERENCES food_categories(id)
        );

        CREATE TABLE IF NOT EXISTS curated_foods(
            id INTEGER PRIMARY KEY,
            food_desc TEXT,
            type TEXT
        );

        CREATE TABLE IF NOT EXISTS prioritized_nutrients(
            id INTEGER PRIMARY KEY,
            category_id REFERENCES nutrient_categories(id),
            priority INTEGER
        );
        """)


        c.execute("""SELECT COUNT(*) FROM food_categories""")
        if not int(c.fetchone()[0]):
            # Migrate
            self.migrate_food_categories()
            self.migrate_nutrient_categories()
            self.migrate_foods()
            self.migrate_food_nutrients()

        # Manually fill in the curated foods
        c.executemany("""INSERT INTO curated_foods VALUES (null, ?, ?)""",
                      [
                          ("Egg", "Breakfast"),
                          ("Cereal", "Breakfast"),
                          ("Bagel", "Breakfast"),

                          ("Salad", "Lunch"),
                          ("Hamburger", "Lunch"),
                          ("Cheeseburger", "Lunch"),
                          ("Sandwich", "Lunch"),
                          ("Wings", "Lunch"),

                          ("Chicken", "Dinner"),
                          ("Fish", "Dinner"),
                          ("Pasta", "Dinner"),
                          ("Steak", "Dinner"),
                          ("Salad", "Dinner"),
                          ("Ravioli", "Dinner"),
                          ("Chili", "Dinner")
                      ])

        # Build indices
        c.execute("""CREATE INDEX IF NOT EXISTS index_food_categories ON food_categories(id);""")
        c.execute("""CREATE INDEX IF NOT EXISTS index_nutrient_categories ON nutrient_categories(id);""")
        c.execute("""CREATE INDEX IF NOT EXISTS index_foods ON foods(id);""")
        c.execute("""CREATE INDEX IF NOT EXISTS index_food_nutrients_junction ON food_nutrients_junction(id, food_id);""")

        # Restrict some categories off the bat
        # Since we assume everyone is older than 8, we can drop the "Baby Food"
        # categories
        self.input_food_restriction(9002)
        self.input_food_restriction(9004)
        self.input_food_restriction(9006)
        self.input_food_restriction(9008)
        self.input_food_restriction(9010)
        self.input_food_restriction(9012)
        self.input_food_restriction(9202)
        self.input_food_restriction(9204)


    def migrate_food_categories(self) -> None:
        c = self.conn.cursor()
        c.execute("""BEGIN TRANSACTION;""")
        with open(DB_CATEGORY_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for id_, description in csv.reader(csvfile):
                id_ = int(id_)
                c.execute("""INSERT INTO food_categories VALUES (?, ?);""", [id_, description])
        c.execute("""COMMIT;""")


    def migrate_nutrient_categories(self) -> None:
        c = self.conn.cursor()
        c.execute("""BEGIN TRANSACTION;""")
        with open(DB_NUTRIENT_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for id_, name, unit, _, _ in csv.reader(csvfile):
                id_ = int(id_)
                c.execute("""INSERT INTO nutrient_categories VALUES (?, ?, ?);""", [id_, name, unit])
        c.execute("""COMMIT;""")


    def migrate_foods(self) -> None:
        c = self.conn.cursor()
        c.execute("""BEGIN TRANSACTION;""")
        with open(DB_FOOD_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            #csvfile.readline()

            for fdc_id, _, description, food_category_id, _ in csv.reader(csvfile):
                fdc_id = int(fdc_id)
                food_category_id = int(food_category_id)
                if food_category_id:
                    c.execute("""INSERT INTO foods VALUES (?, ?, ?, ?);""",
                              [fdc_id, description, food_category_id, 0])
        c.execute("""COMMIT;""")


    def migrate_food_nutrients(self) -> None:
        c = self.conn.cursor()
        c.execute("""BEGIN TRANSACTION;""")
        with open(DB_FOOD_NUTRIENT_LOCATION, 'r', newline='') as csvfile:
            # Drop the first line, which is the header
            csvfile.readline()

            for id_, fdc_id, nutrient_id, amount, *_ in csv.reader(csvfile):
                fdc_id = int(fdc_id)
                nutrient_id = int(nutrient_id)
                amount = float(amount)
                c.execute("""INSERT INTO food_nutrients_junction VALUES (?, ?, ?, ?);""", [id_, fdc_id, nutrient_id, amount])
        c.execute("""COMMIT;""")


    #####
    #
    # Searching
    #
    #####

    def search_food(self, needle: str) -> List[Food]:
        c = self.conn.cursor()

        # NS stands for Not Specified
        # NFS stands for Not Further Specified
        # Anything in parenthesis is likely to be a brand
        # Favor those with less commas (most likely simpler and not hyper specific)
        # Simpler things are also likely to be shorter
        #
        # Chances are, those hyper specific dishes are more likely to have the
        # same category as what the user was searching for, so also sort by the
        # most common category

        # https://stackoverflow.com/questions/3293790/query-to-count-words-sqlite-3
        QUERY="""
                SELECT id, descr,
                    food_category_id, liked,

                    like(:needle || "%", descr) AS is_prefix,
                    like("% NS %", descr) AS is_ns,
                    like("% NFS %", descr) AS is_nfs,
                    like("%(%)", descr) AS has_parenthesis,
                    min(0, length(descr) - length(replace(descr, ',', ''))) AS count_comma,
                    like("%" || :needle || "%", descr) AS is_anywhere,
                    length(descr) AS desc_length,


                    (SELECT descr FROM food_categories WHERE food_categories.id = food_category_id),
                    (SELECT count(*) FROM foods AS f
                     WHERE f.food_category_id = foods.food_category_id
                     AND like("%" || :needle || "%", f.descr))
                    AS category_count,

                    (SELECT count(*) FROM food_exclusion AS f WHERE
                    f.food_category_id = foods.food_category_id) as restricted

                    FROM foods WHERE (is_anywhere AND NOT restricted AND liked
                    >= -3)
                    ORDER BY liked DESC,
                        is_prefix DESC, category_count DESC,
                        is_ns DESC, is_nfs DESC, count_comma DESC,
                        has_parenthesis ASC, descr;
                """

        results = []
        for id_, desc, food_category_id, *_ in c.execute(QUERY, {"needle": needle}):
            results.append(Food(int(id_), desc, int(food_category_id)))

        return results

    def get_food(self, id_: int) -> Food:
        c = self.conn.cursor()

        id_, desc, food_category_id, liked = c.execute("""SELECT * FROM foods WHERE id = ?""", [id_]).fetchone()
        id_ = int(id_)
        food_category_id = int(food_category_id)

        return Food(id_, desc, food_category_id)

    def get_food_category(self, id_: int) -> FoodCategory:
        c = self.conn.cursor()


        id_, desc = c.execute("""SELECT * FROM food_categories WHERE id = ?;""", [id_]).fetchone()
        id_ = int(id_)

        return FoodCategory(id_, desc)

    def get_nutrients(self, id_: int) -> List[Nutrient]:
        c = self.conn.cursor()

        results = []
        for _, _, nutrient_id, amount in c.execute("""SELECT * FROM food_nutrients_junction WHERE food_id = ?""", [id_]):
            results.append(Nutrient(nutrient_id, float(amount)))
        return results

    def get_nutrient_category(self, id_: int) -> NutrientCategory:
        c = self.conn.cursor()

        id_, name, unit = c.execute("""SELECT * FROM nutrient_categories WHERE id = ?""", [id_]).fetchone()
        id_ = int(id_)

        return NutrientCategory(id_, name, unit)


    #####
    #
    # Inputting
    #
    #####

    def input_food_log(self, food_id: int,
                       time: datetime.datetime,
                       type_: FoodType,
                       liked: int = 0) -> None:
        # liked: 0 neutral, 1 yes, 2 no
        c = self.conn.cursor()

        c.execute("""INSERT INTO food_log VALUES (?, ?, ?, ?);""",
                  [None, food_id, time.isoformat(), type_])
        c.execute("""UPDATE foods SET liked = liked + ? WHERE id = ?;""",
                  [liked, food_id])

    def input_food_restriction(self, category_id: int) -> None:
        c = self.conn.cursor()

        c.execute("""INSERT INTO food_exclusion VALUES (?, ?);""",
                  [None, category_id])

    def input_nutrient_prioritization(self, category_id: int, priority: int) -> None:
        c = self.conn.cursor()

        c.execute("""INSERT INTO prioritized_nutrients VALUES (?, ?, ?);""",
                  [None, category_id, priority])

    #####
    #
    # Recommendation
    #
    #####

    def recommend(self, type_: FoodType) -> List[Food]:
        c = self.conn.cursor()

        QUERY="""
                SELECT F.id, F.descr,
                    F.food_category_id, F.liked,

                    (SELECT count(*) FROM food_exclusion AS ff WHERE
                    ff.food_category_id = F.food_category_id) as restricted

                    FROM foods F
                    INNER JOIN curated_foods cur ON like("%" || cur.food_desc ||
                    "%", F.descr) AND cur.type = ?


                    WHERE (NOT restricted AND F.liked = 0)
                    ORDER BY
                        RANDOM()
                """
        results = []
        for id_, desc, food_category_id, *_ in c.execute(QUERY, [type_]):
            results.append(Food(int(id_), desc, int(food_category_id)))

        return results

    def grade(self) -> Tuple[float, List[str]]:
        c = self.conn.cursor()

        #QUERY_START_OF_DAY = """
        #SELECT (SELECT SUM(amount) FROM food_nutrients_junction J WHERE J.food_id = food_log.food_id AND J.nutrient_id = ?)
        #FROM food_log
        #WHERE datetim > datetime('now', 'localtime', 'start of day')"""

        QUERY_START_OF_DAY = """
        SELECT SUM(amount)
        FROM food_nutrients_junction J
        WHERE J.food_id IN
            (SELECT food_id FROM food_log WHERE datetim > datetime('now', 'localtime', 'start of day'))
        AND J.nutrient_id = ?
        """

        QUERY_7_DAYS_AGO = """
        SELECT SUM(amount) / 7
        FROM food_nutrients_junction J
        WHERE J.food_id IN
            (SELECT food_id FROM food_log WHERE datetim > datetime('now', 'localtime', 'start of day', '-7 days'))
        AND J.nutrient_id = ?
        """

        QUERY_30_DAYS_AGO = """
        SELECT SUM(amount) / 30
        FROM food_nutrients_junction J
        WHERE J.food_id IN
            (SELECT food_id FROM food_log WHERE datetim > datetime('now', 'localtime', 'start of day', '-30 days'))
        AND J.nutrient_id = ?
        """

        QUERY_EARLIEST = """SELECT MIN(datetim) FROM food_log LIMIT 1"""

        result = [1]
        messages = []

        c.execute(QUERY_EARLIEST)
        earliest = datetime.datetime.fromisoformat(c.fetchall()[0][0])
        diff = datetime.datetime.now() - earliest
        #print(diff.days)


        for k, v in self.target_daily.items():
            c.execute(QUERY_START_OF_DAY, (int(k), ))
            sum_amount = c.fetchall()[0][0]

            #print(k, v, sum_amount)
            if abs(v - sum_amount) > v * 0.5:
                result[0] = max(result[0] - 0.05, 0)

                if v - sum_amount > 0:
                    messages.append(f"Significantly increase consumption of {self.friendly_nutrient_names[k]}-rich foods")
                else:
                    messages.append(f"Significantly reduce consumption of {self.friendly_nutrient_names[k]}-rich foods")
            elif abs(v - sum_amount) > v * 0.15:
                result[0] = max(result[0] - 0.01, 0)

                if v - sum_amount > 0:
                    messages.append(f"Increase consumption of {self.friendly_nutrient_names[k]}-rich foods")
                else:
                    messages.append(f"Reduce consumption of {self.friendly_nutrient_names[k]}-rich foods")

        if diff.days >= 7:
            result.append(1)
            for k, v in self.target_daily.items():
                c.execute(QUERY_7_DAYS_AGO, (int(k), ))
                sum_amount = c.fetchall()[0][0]

                #print(k, v, sum_amount)
                if abs(v - sum_amount) > v * 0.5:
                    result[1] = max(result[1] - 0.05, 0)
                elif abs(v - sum_amount) > v * 0.15:
                    result[1] = max(result[1] - 0.01, 0)


        if diff.days >= 30:
            result.append(1)
            for k, v in self.target_daily.items():
                c.execute(QUERY_30_DAYS_AGO, (int(k), ))
                sum_amount = c.fetchall()[0][0]

                #print(k, v, sum_amount)
                if abs(v - sum_amount) > v * 0.5:
                    result[2] = max(result[2] - 0.05, 0)
                elif abs(v - sum_amount) > v * 0.15:
                    result[2] = max(result[2] - 0.01, 0)


        return (sum(result)/len(result), messages)






def main():
    db = Database()

    beginning = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Eat bagel for breakfast
    db.input_food_log(1100713, beginning + datetime.timedelta(hours=8), "Breakfast")
    # Cream cheese
    db.input_food_log(1098057, beginning + datetime.timedelta(hours=8), "Breakfast")
    # Drink apple juice too
    db.input_food_log(1102747, beginning + datetime.timedelta(hours=8), "Breakfast")
    # Eat Pasta with tomato-based sauce and poultry, ready-to-heat
    db.input_food_log(1102230, beginning + datetime.timedelta(hours=13), "Lunch")
    # Drink Soft drink, cola
    db.input_food_log(1104310, beginning + datetime.timedelta(hours=13), "Lunch")
    # Eat Apple, raw
    db.input_food_log(1102644, beginning + datetime.timedelta(hours=15), "Snack")
    db.input_food_log(1102644, beginning + datetime.timedelta(hours=17), "Snack")
    # Eat Beef steak, braised, lean and fat eaten
    db.input_food_log(1098183, beginning + datetime.timedelta(hours=18), "Dinner")
    # Eat Potato, mashed, from dry mix, made with milk
    db.input_food_log(1103004, beginning + datetime.timedelta(hours=18), "Dinner")

    print(db.grade())


    db.recommend("Lunch")
    print(db.recommend("Lunch"))

    line = input("Food> ")
    while (line):
        for i, row in enumerate(db.search_food(line)):
            print(f"{row.fdc_id}   {row.description:30}")

            if i % 10 == 9:
                inp = input("More or enter ID> ")
                if inp and inp != "More":
                    inp = int(inp)
                    _, desc, food_category_id = db.get_food(inp)
                    _, category_desc = db.get_food_category(food_category_id)
                    nutrients = db.get_nutrients(inp)

                    print(f"Food: {desc}")
                    print(f"Food category ({food_category_id}): {category_desc}")
                    for nutrient_id, nutrient_amount in nutrients:
                        if nutrient_amount < 0.1: continue

                        _, nutrient_name, unit = db.get_nutrient_category(nutrient_id)
                        print(f"{nutrient_name}: {nutrient_amount} {unit}")
                    break
        line = input("Food> ")



if __name__ == "__main__":
    main()

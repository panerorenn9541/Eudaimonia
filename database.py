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

    def __init__(self, location="temp.db") -> None:
        self.conn = connect(location)
        self.migrate()


    #####
    #
    # Migration
    #
    #####

    def migrate(self) -> None:
        c = self.conn.cursor()
        c.execute("""PRAGMA foreign_keys = ON;""")

        # Create the tables
        c.execute("""CREATE TABLE food_categories(id INTEGER PRIMARY KEY, descr TEXT);""")
        c.execute("""CREATE TABLE nutrient_categories(id INTEGER PRIMARY KEY, name TEXT, unit TEXT);""")
        c.execute("""CREATE TABLE foods(
                        id INTEGER PRIMARY KEY,
                        descr TEXT,
                        food_category_id INTEGER,
                        liked INTEGER,
                        FOREIGN KEY(food_category_id) REFERENCES food_categories(id)
                  );""")
        c.execute("""CREATE TABLE food_nutrients_junction(
                        id INTEGER PRIMARY KEY,
                        food_id INTEGER REFERENCES foods(id),
                        nutrient_id INTEGER REFERENCES nutrient_categories(id),
                        amount REAL
                    );""")
        c.execute("""CREATE TABLE food_log(
                        id INTEGER PRIMARY KEY,
                        food_id INTEGER REFERENCES foods(id),
                        datetim TEXT,
                        type TEXT);""")
        c.execute("""CREATE TABLE food_exclusion(
                        id INTEGER PRIMARY KEY,
                        food_category_id INTEGER REFERENCES
                        food_categories(id));""")
        c.execute("""CREATE TABLE curated_foods(
                        id INTEGER PRIMARY KEY,
                        food_desc TEXT,
                        type TEXT);""")
        c.execute("""CREATE TABLE prioritized_nutrients(
                        id INTEGER PRIMARY KEY,
                        category_id REFERENCES nutrient_categories(id),
                        priority INTEGER);""")

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
        c.execute("""CREATE INDEX index_food_categories ON food_categories(id);""")
        c.execute("""CREATE INDEX index_nutrient_categories ON nutrient_categories(id);""")
        c.execute("""CREATE INDEX index_foods ON foods(id);""")
        c.execute("""CREATE INDEX index_food_nutrients_junction ON food_nutrients_junction(id, food_id);""")


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
            #print(id_, desc, food_category_id, _)
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
                       type_: Literal["Breakfast", "Lunch", "Dinner", "Snack"],
                       liked: int = 0) -> None:
        # liked: 0 neutral, 1 yes, 2 no
        c = self.conn.cursor()

        c.execute("""INSERT INTO food_log VALUES (?, ?, ?, ?)""",
                  [None, food_id, time.isoformat(), type_])
        c.execute("""UPDATE foods SET liked = liked + ? WHERE id = ?""",
                  [liked, food_id])

    def input_food_restriction(self, category_id: int) -> None:
        c = self.conn.cursor()

        c.execute("""INSERT INTO food_exclusion VALUES (?, ?)""",
                  [None, category_id])

    def input_nutrient_prioritization(self, category_id: int, priority: int) -> None:
        c = self.conn.cursor()

        c.execute("""INSERT INTO prioritized_nutrients VALUES (?, ?, ?)""",
                  [None, category_id, priority])

    #####
    #
    # Recommendation
    #
    #####

    def recommend(self, type_: Literal["Breakfast", "Lunch", "Dinner", "Snack"]) -> List[Food]:
        c = self.conn.cursor()

        QUERY="""
                SELECT F.id, F.descr,
                    F.food_category_id, F.liked,

                    (SELECT count(*) FROM food_exclusion AS ff WHERE
                    ff.food_category_id = F.food_category_id) as restricted,

                    (SELECT sum(amount) FROM food_nutrients_junction AS ff
                    INNER JOIN prioritized_nutrients P ON ff.nutrient_id =
                    P.category_id
                    WHERE ff.food_id = F.id LIMIT 1) as prio

                    FROM foods F
                    INNER JOIN curated_foods cur ON like("%" || cur.food_desc ||
                    "%", F.descr) AND cur.type = ?

                    JOIN prioritized_nutrients P
                    JOIN food_nutrients_junction ON food_nutrients_junction.food_id = F.id AND P.category_id = food_nutrients_junction.nutrient_id

                    WHERE (NOT restricted AND liked = 0 AND prio > 0 AND food_nutrients_junction.amount > 0.1)
                    ORDER BY
                        P.priority DESC, food_nutrients_junction.amount DESC,
                        RANDOM();
                """
        results = []
        for id_, desc, food_category_id, *_ in c.execute(QUERY, [type_]):
            print(id_, desc, food_category_id, _)
            results.append(Food(int(id_), desc, int(food_category_id)))

        return results






def main():
    db = Database()
    # Soups
    db.input_food_restriction(3802)
    # Baby foods
    db.input_food_restriction(9002)
    db.input_food_restriction(9004)
    db.input_food_restriction(9006)
    db.input_food_restriction(9008)
    db.input_food_restriction(9010)
    db.input_food_restriction(9012)
    db.input_food_restriction(9202)
    db.input_food_restriction(9204)

    # I absolutely hate raw tomatoes! (not true)
    db.input_food_log(1103276, datetime.datetime.now(), "Snack", -3)
    # But I like pasta with tomato-based sauce and cheese
    db.input_food_log(1102211, datetime.datetime.now(), "Snack", 1)

    # Prioritize iron intake, then protein
    db.input_nutrient_prioritization(1089, 2)
    db.input_nutrient_prioritization(1003, 1)

    db.recommend("Lunch")
    #print(db.recommend("Lunch"))

    while (line := input("Food> ")):
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



if __name__ == "__main__":
    main()

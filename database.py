from typing import *
from dataclasses import dataclass
from sqlite3 import connect, Connection
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
                        FOREIGN KEY(food_category_id) REFERENCES food_categories(id)
                  );""")
        c.execute("""CREATE TABLE food_nutrients_junction(
                        id INTEGER PRIMARY KEY,
                        food_id INTEGER REFERENCES foods(id),
                        nutrient_id INTEGER REFERENCES nutrient_categories(id),
                        amount REAL
                    );""")

        # Migrate
        self.migrate_food_categories()
        self.migrate_nutrient_categories()
        self.migrate_foods()
        self.migrate_food_nutrients()

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
                    c.execute("""INSERT INTO foods VALUES (?, ?, ?);""", [fdc_id, description, food_category_id])
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
                    food_category_id,

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
                    AS category_count

                    FROM foods WHERE is_anywhere ORDER BY
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

        id_, desc, food_category_id = c.execute("""SELECT * FROM foods WHERE id = ?""", [id_]).fetchone()
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




def main():
    db = Database()
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
                    print(f"Food category: {category_desc}")
                    for nutrient_id, nutrient_amount in nutrients:
                        if nutrient_amount < 0.1: continue

                        _, nutrient_name, unit = db.get_nutrient_category(nutrient_id)
                        print(f"{nutrient_name}: {nutrient_amount} {unit}")
                    break



if __name__ == "__main__":
    main()

import csv

FOOD_IN="""/home/user/work/cs125/Eudaimonia/db/food.csv"""
FOOD_OUT="""/home/user/work/cs125/Eudaimonia/db/food_reduced.csv"""

with open(FOOD_IN, 'r', newline='') as csvfile:
    with open(FOOD_OUT, 'w', newline='') as newfile:
        csvfile.readline()

        csvwriter = csv.writer(newfile)
        for r in csv.reader(csvfile):
            if r[3]:
                csvwriter.writerow(r)

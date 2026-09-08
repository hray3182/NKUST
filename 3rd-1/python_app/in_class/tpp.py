import sqlite3
import csv

con = sqlite3.connect("populations.db")
cur = con.cursor()

# cur.execute("""CREATE TABLE populations(
#    area TEXT,
#    male INT,
#    femail INT,
#    total INT
# )""")

file_name = "taipei-population.csv"

with open(file_name, "r", encoding="utf-8-sig") as csvFile:
    reader = csv.reader(csvFile)
    listCsv = list(reader)
    csvData = listCsv[4:]
    for row in csvData:
        print(row[0])
        area = row[0]
        male = row[7]
        female = row[8]
        total = row[6]
        cur.execute(
            "insert into populations value(?,?,?,?)", (area, male, female, total)
        )
        con.commit()

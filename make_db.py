## db.sqliteを作成するスクリプト
## ファイルの構成は次の通りになっている必要がある
## exams
## │  db.sqlite
## │
## ├─力学B
## │      力学B_2019.pdf
## │      力学B_2020.pdf
## │      力学B_2020_1.pdf
## │      力学B_2021.pdf
## │      力学B_2021_1.pdf
## │
## ├─力学演習
## │      力学演習_2020.pdf
## │      力学演習_2021.pdf
## │      力学演習_2021_1.pdf
## │      力学演習_2021_2.pdf
## │
## ├─固体物理学I
## │      固体物理学I_2021.pdf
## │      固体物理学I_2023.pdf
## │
## ├─宇宙天体物理学
## │      宇宙天体物理学_2022.pdf

import glob
import sqlite3

files = glob.glob("exams/**/*")

for file in files:
    print(file)

conn = sqlite3.connect("exams/db.sqlite")
cur = conn.cursor()

table = f"""CREATE TABLE IF NOT EXISTS exam_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT,
            year INTEGER,
            path TEXT
            )"""

cur.execute(table)

for file in files:
    if ".pdf" in file:
        filename = file.split("\\")[-1]
        course = filename.split("_")[0]
        year = filename.split("_")[1].split(".")[0]
        cur.execute("INSERT INTO exam_table (course, year, path) VALUES (?, ?, ?)", (course, year, file))

conn.commit()
conn.close()
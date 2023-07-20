import sqlite3

db = sqlite3.connect('./database.sqlite')
# tableの作成
table_name = 'pastexam'
cur = db.cursor()
table = f"""create table if not exists {table_name} 
    (id     integer primary key autoincrement,
    name    text,
    year    integer,
    path    text)"""
cur.execute(table)

import sqlite3

conn = sqlite3.connect("instance/flask_db.sqlite")

for i in conn.execute("SELECT * FROM people").fetchall():
    print(i)

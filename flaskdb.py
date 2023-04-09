import os
import sqlite3
import click
from flask import Flask, g, request

app = Flask(__name__)
DATA_PATH = os.path.join(app.instance_path, 'flask_db.sqlite')

people = [('Abraham', '1', 'Be\'er Sheva'),
          ('Isaac', '1', 'Be\'er Sheva'),
          ('Jacob', '3', 'Shkhem'),
          ('Joseph', '4', 'Goshen'),
          ('Moses', '1', 'Sinai'),
          ('Aharon', '6', 'Hor Hahar'),
          ('David', '7', 'Jerusalem')]


def db_to_str(db_res):
    res = []
    for item in db_res:
        res.extend([{'name': item['name'], 'id': str(item['id']), 'address': item['address']}])
    return res


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATA_PATH)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()


@app.route("/")
def select_elements():
    name, id_, address = request.headers.get('name'),\
                         request.headers.get('Id'),\
                         request.headers.get('Address')
    db: sqlite3.dbapi2 = get_db()

    res = db.cursor().execute("SELECT * FROM people WHERE (:name IS NULL OR name = :name) AND\
                                                          (:id IS NULL OR id = :id) AND\
                                                          (:address IS NULL OR address = :address);",
                              {'name': name, 'id': id_, 'address': address}).fetchall()

    print(res)
    return db_to_str(res)


@click.command("init-db")
def init_command():
    db = get_db()
    db.executescript('''
    DROP TABLE IF EXISTS people;
    CREATE TABLE people (name STRING, id INTEGER, address STRING);
    ''')
    for i in people:
        db.execute("INSERT INTO people VALUES (?, ?, ?);", i)
        db.commit()
    click.echo("Database initialized.")


app.cli.add_command(init_command)

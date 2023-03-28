import sqlite3
from dbutils import Database
from flask import Flask, g
from markupsafe import escape

app = Flask(__name__)
DATA_PATH = ':memory:'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATA_PATH)
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def insert(self, p: Database.Person):
    query_db(''' INSERT INTO people VALUES (:name, :id, :address) ''',
             {'name': p.name, 'id': p.id, 'address': p.address})


def update(self, id_: str, p: Database.Person):
    query_db(''' UPDATE people SET address = :address, name = :name WHERE id = :id ''',
             {'name': p.name, 'id': p.id, 'address': p.address})


def delete(self, id_: str):
    query_db(''' DELETE FROM people WHERE id = :id ''',
             {'id': id_})


def present(self):
    return query_db(''' SELECT * FROM people ''')



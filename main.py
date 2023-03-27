import sqlite3
from dbutils import Database

conn = sqlite3.connect(':memory:')

# from flask import Flask, g
# from markupsafe import escape
#
# DATA_PATH = ':memory:'
#
# app = Flask(__name__)
#
#
# @app.route('/<string:path>-<int:num>')
# def hello(path, num):
#     return f'<p>Hello, this is {escape(path)} with param {num}</p>'
#
#
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATA_PATH)
#     db.row_factory = sqlite3.Row
#     return db
#
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


people = [Database.Person('Abraham', '1', 'Be\'er Sheva'),
          Database.Person('Isaac', '2', 'Grar'),
          Database.Person('Jacob', '3', 'Shkhem'),
          Database.Person('Joseph', '4', 'Goshen'),
          Database.Person('Moses', '5', 'Sinai')]


if __name__ == '__main__':
    d = Database(conn)

    inp = None
    while inp != 'exit':
        inp = input('enter command (1-insert, 2-update, 3-delete: ')
        if inp == '1':
            y = int(input('enter person number (1-5): '))
            d.insert(people[y - 1])
        elif inp == '2':
            y = people[int(input('enter person number to update(1-5): ')) - 1].id
            n_name = input('enter updated name: ')
            n_add = input('enter updated address: ')
            d.update(y, Database.Person(n_name, y, n_add))
        elif inp == '3':
            y = people[int(input('enter person number to delete (1-5): ')) - 1].id
            d.delete(y)

        conn.commit()
        print(d.present())

    conn.close()

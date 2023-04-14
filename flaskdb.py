import sqlite3
from logging import Logger, FileHandler, Formatter
from flask import g, request, current_app, Blueprint

bp = Blueprint("db_operations", __name__)

logger = Logger(__name__)
logger.setLevel('INFO')

formatter = Formatter(f'%(name)s entry; func "%(funcName)s": %(message)s')

log_handler = FileHandler('db_log.log')
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)


people = [('Abraham', '1', 'Be\'er Sheva'),
          ('Isaac', '2', 'Grar'),
          ('Jacob', '3', 'Shkhem'),
          ('Joseph', '4', 'Goshen'),
          ('Moses', '5', 'Sinai'),
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
        db = g.database = sqlite3.connect(current_app.config['DATABASE'])
        if not db.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='people'").fetchone()[0]:
            db.executescript('''
                DROP TABLE IF EXISTS people;
                CREATE TABLE people (name STRING, id INTEGER, address STRING);
                ''')

            logger.info('Database created.')

            for i in people:
                db.execute("INSERT INTO people VALUES (?, ?, ?);", i)
                db.commit()

            logger.info('Database initialized with values')
    db.row_factory = sqlite3.Row
    return db


def close_connection(e):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()


@bp.route("/", methods=('GET', 'POST'))
def select_elements():
    name, id_, address = request.headers.get('name'),\
                         request.headers.get('Id'),\
                         request.headers.get('Address')
    db = get_db()

    logger.info(f'Accepted {request.method} request with parameters ({name}, {id_}, {address})')

    if request.method == 'GET':
        res = db.cursor().execute("SELECT * FROM people WHERE (:name IS NULL OR name = :name) AND\
                                                              (:id IS NULL OR id = :id) AND\
                                                              (:address IS NULL OR address = :address);",
                                  {'name': name, 'id': id_, 'address': address}).fetchall()

        return db_to_str(res)
    if not (name and id_ and address):
        logger.warning(f'Some values weren\'t accepted. Fields will be padded with NaN')

    db.execute("INSERT INTO people VALUES (?, ?, ?)", (name, id_, address))
    db.commit()

    return "Data inserted successfully.\n"


@bp.route("/", methods=('POST', ))
def insert_element():
    name, id_, address = request.headers.get('name'),\
                         request.headers.get('Id'),\
                         request.headers.get('Address')
    db = get_db()

    if name and id_ and address:
        logger.info(f'Accepted POST request with parameters ({name}, {id_}, {address})')



def init_app(app):
    app.teardown_appcontext(close_connection)

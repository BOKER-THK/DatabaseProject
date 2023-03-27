class Database:

    class Person:
        name: str
        id: str
        address: str

        def __init__(self, name, id_, address):
            self.name = name
            self.id = id_
            self.address = address

        def __str__(self):
            return self.id + ', ' + self.name + ': ' + self.address

    def __init__(self, conn):
        self.c = conn.cursor()

        # Check if table "people" already exists, and if not - create it
        self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='people' ''')
        if self.c.fetchone()[0] < 1:
            self.c.execute(''' CREATE TABLE people (name text, id text, address text) ''')

    def insert(self, p: Person):
        self.c.execute(''' INSERT INTO people VALUES (:name, :id, :address) ''',
                       {'name': p.name, 'id': p.id, 'address': p.address})

    def update(self, id_: str, p: Person):
        self.c.execute(''' UPDATE people SET address = :address, name = :name WHERE id = :id ''',
                       {'name': p.name, 'id': p.id, 'address': p.address})

    def delete(self, id_: str):
        self.c.execute(''' DELETE FROM people WHERE id = :id ''',
                       {'id': id_})

    def present(self):
        self.c.execute(''' SELECT * FROM people ''')
        return self.c.fetchall()

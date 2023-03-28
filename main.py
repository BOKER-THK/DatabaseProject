import sqlite3
from dbutils import Database

conn = sqlite3.connect(':memory:')

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

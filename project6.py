from sqlite3 import*
db_connect = connect('project666.db')
db_cursor = db_connect.cursor() 
#h
def create_table():
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS readers
                      (pr TEXT PRIMARY KEY,
                      full_name TEXT NOT NULL,
                      phone TEXT NOT NULL,
                      age INTEGER NOT NULL
                      )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS books
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      author TEXT NOT NULL,
                      genre TEXT NOT NULL,
                      total INTEGER NOT NULL CHECK(total >= 1),
                      free INTEGER NOT NULL CHECK(free >= 0 and free <=total) )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS loans 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      date TEXT NOT NULL CHECK(date GLOB '[0-3][0-9]/[0-1][0-9]/[0-9][0-9]')
                     )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS holds
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      date TEXT NOT NULL CHECK(date GLOB '[0-3][0-9]/[0-1][0-9]/[0-9][0-9]')
                      )""")
    db_cursor.execute('''SELECT * FROM books''')
    print(db_cursor.fetchall())
    db_connect.commit()
create_table()

db_cursor.execute('''SELECT * FROM books''')
print(db_cursor.fetchall())

#db_connect.close()

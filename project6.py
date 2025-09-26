import sqlite3
db_connect = sqlite3.connect('project666.db')
db_cursor = db_connect.cursor() 
#h
def create_table():
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS readers
                      (pr TEXT PRIMARY KEY,
                      full_name TEXT NOT NULL,
                      password TEXT NOT NULL,
                      phone TEXT NOT NULL,
                      age INTEGER NOT NULL
                      )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS books
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      author TEXT NOT NULL,
                      genre INTEGER NOT NULL CHECK(total >=1),
                      free INTEGER NOT NULL CHECK(free >= 0 and free <=total)
                      )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS loans 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id)
                     )""")
    db_cursor.execute("""CREATE TABLE IF NOT EXISTS holds
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pr TEXT NOT NULL REFERENCES readers(pr),
                      book_id INTEGER NOT NULL REFERENCES books(id),
                      date TEXT NOT NULL 
                      )""")
    db_connect.commit()
create_table()
db_connect.close()
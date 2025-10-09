from repo import*
db_connect = connect('project666.db')
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
                      genre INTEGER NOT NULL,
                      free INTEGER NOT NULL )""")
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
   
    print(db_cursor.fetchall())
    
    db_connect.commit()
create_table()
db_cursor.execute('''SELECT * FROM books''')
print(db_cursor.fetchall())
#delete_book(db_connect, "book1", "author1")

db_cursor.execute('''INSERT INTO books VALUES (1, 'book1', 'author1', 1, 0)''')
db_cursor.execute('''SELECT * FROM books''')
db_connect.close()
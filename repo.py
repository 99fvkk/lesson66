from sqlite3 import*
cursor = connect('project666.db').cursor() 
def add_reader(full_name, phone, age):
    cursor.execute('')
def delete_book(title, author):
    cursor.execute('SELECT id FROM books WHERE title=? AND author=? AND free = 0', 
                   (title, author))
    id_1=cursor.fetchall()

    cursor.execute(f'DELETE FROM books WHERE id = {id_1[0][0]}')
    cursor.execute('SELECT * FROM books')
    print(cursor.fetchall()) 
delete_book()
add_reader()
def delete_reader(full_name, phone, age):
    cursor.execute('SELECT id FROM reader WHERE full_name=? AND phone=? AND age=? IF NOT NULL', 
                   (full_name, phone, age))
    id_2=cursor.fetchall() 
    cursor.execute(f'DELETE FROM reader WHERE id = {id_2[0][0]}')
    cursor.execute('SELECT * FROM reader')
    print(cursor.fetchall())
delete_reader()



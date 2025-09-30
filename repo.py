from sqlite3 import*

def delete_book(conn, title, author):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM books WHERE title=? AND author=? AND free = 0''', 
                   (title, author))
    id_1=cursor.fetchall()

    cursor.execute(f'''DELETE FROM books WHERE id = {id_1[0][0]}''')
    cursor.execute('''SELECT * FROM books''')
    print(cursor.fetchall())


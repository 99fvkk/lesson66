from sqlite3 import*
def hold_book(conn, pr , title, author, date):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM books WHERE title=? AND author=? WHERE FREE > 0'''
                   (title, author))
    id_1=cursor.fetchall()
    cursor.execute(f'''UPDATE books SET free-=1 WHERE id={id_1[0][0]}''')
    cursor.execute('SELECT * FROM holds')
    holds=cursor.fetchall()
    cursor.execute('''INSERT INTO holds VALUES(id = ?, pr=?, book_id=?, date = ?)'''
                   (len(holds)+1,  pr, id_1[0][0], date))
def cancel_hold(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute(f'''SELECT id FROM books WHERE title={title}, author={author}''')
    book_id=cursor.fetchall()
    cursor.execute(f'''DELETE FROM holds WHERE id = {book_id[0][0]} AND pr={pr}''')
    cursor.execute(f'''UPDATE books SET free+=1  WHERE title={title}, author={author}''')

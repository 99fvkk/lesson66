from sqlite3 import*
from datetime import datetime

def borrow_book(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute('''SELECT id, free FROM books WHERE title=? AND author=?''',
                   (title, author))
    book_id, free = cursor.fetchone()
    if free==0:
        print('Вы не можете взять книгу')
        return False
    cursor.execute('''SELECT id FROM holds WHERE pr=? AND book_id=?''',
                   (pr, book_id))
    cursor.execute('''SELECT COUNT(*) FROM loans WHERE pr=?''',
                   (pr,))
    
    if cursor.fetchone()[0]>=5:
        print('Читатель не может взять книгу т.к. у него более 5 активных броней')
        return False
    if cursor.fetchone()[0]:
        cursor.execute('''DELETE FROM holds WHERE pr=? AND book_id=?''',
                       (pr, book_id))
    cursor.execute('''SELECT COUNT(*) FROM loans''')
    id_1=cursor.fetchone()[0]+1
    current_date=datetime.now().strftime("%d/%m/%y")
    cursor.execute('''INSERT INTO loans VALUES id=?, pr=?, book_id=?, date=?''',
                   (id_1, pr, book_id, current_date))
    conn.commit()
    return True

def hold_book(conn, pr , title, author, date):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM books WHERE title=? AND author=? AND free > 0'''
                   (title, author))
    id_1=cursor.fetchall()
    cursor.execute(f'''UPDATE books SET free-=1 WHERE id={id_1[0][0]}''')
    cursor.execute('SELECT * FROM holds')
    holds=cursor.fetchall()
    cursor.execute('''INSERT INTO holds VALUES(id = ?, pr=?, book_id=?, date = ?)'''
                   (len(holds)+1,  pr, id_1[0][0], date))
    conn.commit()
    return True
    
def cancel_hold(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute(f'''SELECT id FROM books WHERE title={title} AND author={author}''')
    book_id=cursor.fetchall()
    cursor.execute(f'''DELETE FROM holds WHERE id = {book_id[0][0]} AND pr={pr}''')
    cursor.execute(f'''UPDATE books SET free+=1  WHERE title={title} AND author={author}''')
    conn.commit()
    return True

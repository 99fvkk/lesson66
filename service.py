from sqlite3 import*
from datetime import datetime

def find_book(conn, title=None, author=None, genre=None):
    cursor=conn.cursor()
    query='''SELECT title, author, genre, total, free FROM books WHERE 1=1'''
    params=[]
    if title:
        query1=''' AND LOWER(title)=LOWER(?)'''
        params.append(title)
        query=query+query1
    if author:
        query2=''' AND LOWER(author)=LOWER(?)'''
        params.append(author)
        query=query+query2
    if genre:
        query3=''' AND LOWER(genre)=LOWER(?)'''
        params.append(genre)
        query=query+query3
    cursor.execute(query, params)
    return True

def borrow_book(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute('''SELECT book_id, free FROM books WHERE title=? AND author=?''',
                   (title, author))
    book_id, free = cursor.fetchone()
    if free==0:
        print('Вы не можете взять книгу')
        return False
    cursor.execute('''SELECT id FROM holds WHERE pr=? AND book_id=?''',
                   (pr, book_id))
    cursor.execute('''SELECT COUNT(*) FROM loans WHERE pr=?''',
                   (pr))
    if cursor.fetchone()>=5:
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
    return True

from sqlite3 import*
from datetime import datetime, timedelta, date

def hold_book(conn, pr , title, author, date):
    cursor=conn.cursor()
    cursor.execute("""SELECT id FROM books WHERE title=? AND author=? WHERE FREE > 0"""
                   ,(title, author))
    id_1=cursor.fetchall()
    cursor.execute(f"""UPDATE books SET free-=1 WHERE id={id_1[0][0]}""")
    cursor.execute('SELECT * FROM holds')
    holds=cursor.fetchall()
    cursor.execute("""INSERT INTO holds VALUES(id = ?, pr=?, book_id=?, date = ?)""",(len(holds)+1,  pr, id_1[0][0], date))
    conn.commit()

    
def cancel_hold(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute(f"""SELECT id FROM books WHERE title={title}, author={author}""")
    book_id=cursor.fetchall()
    cursor.execute(f"""DELETE FROM holds WHERE id = {book_id[0][0]} AND pr={pr}""")
    cursor.execute(f"""UPDATE books SET free+=1  WHERE title={title}, author={author}""")
    conn.commit()


def borrow_book(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute("""SELECT book_id, free FROM books WHERE title=? AND author=?""", (title, author))
    book_id, free = cursor.fetchone()
    if free==0:
        print('Вы не можете взять книгу')
        return False
    cursor.execute("""SELECT id FROM holds WHERE pr=? AND book_id=?""", (pr, book_id))
    cursor.execute("""SELECT COUNT(*) FROM loans WHERE pr=?""",(pr))
    if cursor.fetchone()>=5:
        print('Читатель не может взять книгу т.к. у него более 5 активных броней')
        return False
    if cursor.fetchone()[0]:
        cursor.execute("""DELETE FROM holds WHERE pr=? AND book_id=?""",
                       (pr, book_id))
    cursor.execute("""SELECT COUNT(*) FROM loans""")
    id_1=cursor.fetchone()[0]+1
    current_date=datetime.now().strftime("%d/%m/%y")
    cursor.execute("""INSERT INTO loans VALUES id=?, pr=?, book_id=?, date=?""",
                   (id_1, pr, book_id, current_date))
    conn.commit()
    return True


def return_book(conn, pr, title, author):
    cursor=conn.cursor()
    cursor.execute("""SELECT book_id FROM books WHERE title=? AND author=?""", (title, author))
    book_id = cursor.fetchone()
    cursor.execute("""DELETE FROM loans WHERE pr=? AND book_id=?""",(pr, book_id,))
    cursor.execute(f"""UPDATE books SET free+=1  WHERE title={title}, author={author}""")
    conn.commit()


def overdue_list(conn):
    cursor=conn.cursor()
    cursor.execute('''SELECT loans.pr, readers.full_name, books.title, books.author, loans.date as date_borrowed,
                    date(loans.date, '+14 days') as date_return
                    FROM loans
                    JOIN readers ON loans.pr=readers.pr 
                    JOIN books ON loans.book_id=books.id 
                    WHERE date('now') > date(loans.date, '+14 days')''',
                    )
    overdue = cursor.fetchall()
    return overdue

def autocancel(conn):
    cursor=conn.cursor()
    today=datetime.now()
    cursor.execute('''SELECT id, book_id, date FROM holds''')
    holds_table=cursor.fetchall()
    for hold_item in holds_table:
        if today>=hold_item[2]+timedelta(days=5):
            cursor.execute('''DELETE FROM holds WHERE id=?''',
                           (hold_item[0]))
            cursor.execute('''UPDATE books WHERE id=? SET free=free+1''',
                           (hold_item[1]))
    return True
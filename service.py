from sqlite3 import*
from datetime import datetime, timedelta, date

def hold_book(conn, pr, title, author):
    db_cursor = conn.cursor()
    db_cursor.execute("""SELECT COUNT(*) FROM holds WHERE pr=?""", (pr,))
    current_holds_count = db_cursor.fetchone()[0]
    if current_holds_count >= 5:
        return False, "Превышен лимит бронирования (максимум 5 книг)"
    
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=? AND free > 0""",
                   (title, author))
    book = db_cursor.fetchone()
    if book:
        book_id = book[0]
        current_date = datetime.now().strftime("%d/%m/%y")
        db_cursor.execute("""UPDATE books SET free = free - 1 WHERE id=?""", (book_id,))
        db_cursor.execute("""INSERT INTO holds (pr, book_id, date) VALUES (?, ?, ?)""",
                       (pr, book_id, current_date))
        conn.commit()
        return True, "Книга успешно забронирована"
    else:
        return False, "Книга недоступна для бронирования"
    
def cancel_hold(conn, pr, title, author):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    book_id=db_cursor.fetchone()[0]
    print(book_id)
    db_cursor.execute("""DELETE FROM holds WHERE book_id=? AND pr=?""", (book_id, pr))
    db_cursor.execute("""UPDATE books SET free=free+1 WHERE title=? AND author=?""", (title, author))
    conn.commit()


def borrow_book(conn, pr, title, author):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT id, free FROM books WHERE title=? AND author=?""", (title, author))
    book_id, free = db_cursor.fetchone()
    if free==0:
        print('Вы не можете взять книгу')
        return False
    db_cursor.execute("""SELECT COUNT(*) FROM loans WHERE pr=?""",(pr,))
    count_loans=db_cursor.fetchone()[0]
    if count_loans>=5:
        print('Читатель не может взять книгу т.к. у него более 5 активных броней')
        return False
    if count_loans:
        db_cursor.execute("""DELETE FROM holds WHERE pr=? AND book_id=?""",
                       (pr, book_id))
    current_date=datetime.now().strftime("%d/%m/%y")
    db_cursor.execute("""INSERT INTO loans (pr, book_id, date) VALUES (?, ?, ?)""",
                   (pr, book_id, current_date))
    db_cursor.execute("""UPDATE books SET free=free-1 WHERE title=? AND author=?""", (title, author))
    conn.commit()
    return True


def return_book(conn, pr, title, author):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT book_id FROM books WHERE title=? AND author=?""", (title, author))
    book_id = db_cursor.fetchone()
    db_cursor.execute("""DELETE FROM loans WHERE pr=? AND book_id=?""",(pr, book_id,))
    db_cursor.execute(f"""UPDATE books SET free+=1  WHERE title={title}, author={author}""")
    conn.commit()


def overdue_list(conn):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT loans.pr, readers.full_name, books.title, books.author, loans.date as date_borrowed,
                    date(loans.date, '+14 days') as date_return
                    FROM loans
                    JOIN readers ON loans.pr=readers.pr 
                    JOIN books ON loans.book_id=books.id 
                    WHERE date('now') > date(loans.date, '+14 days')""",
                    )
    overdue = db_cursor.fetchall()
    return overdue

def autocancel(conn):
    db_cursor=conn.cursor()
    today=datetime.now()
    db_cursor.execute("""SELECT id, book_id, date FROM holds""")
    holds_table=db_cursor.fetchall()
    for hold_item in holds_table:
        if today>=hold_item[2]+timedelta(days=5):
            db_cursor.execute("""DELETE FROM holds WHERE id=?""",
                           (hold_item[0]))
            db_cursor.execute("""UPDATE books WHERE id=? SET free=free+1""",
                           (hold_item[1]))
    return True


def return_holds(conn, pr):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT books.title, books.author, holds.date
                      FROM holds 
                      JOIN books ON holds.book_id=books.id
                      WHERE holds.pr=?""", (pr,))
    holds_items=db_cursor.fetchall()
    holds_list=[]
    for hold_item in holds_items:
        holds_list.append([hold_item[0], hold_item[1], hold_item[2], datetime.strftime(datetime.strptime(hold_item[2], "%d/%m/%y")+timedelta(days=5), "%d/%m/%y")])
    return holds_list

def return_loans(conn, pr):
    db_cursor=conn.cursor()
    db_cursor.execute("""SELECT books.title, books.author, loans.date
                      FROM loans
                      JOIN books ON loans.book_id=books.id
                      WHERE loans.pr=?""", (pr,))
    loans_items=db_cursor.fetchall()
    loans_list=[]
    for loan_item in loans_items:
        loans_list.append([loan_item[0], loan_item[1], loan_item[2], datetime.strftime(datetime.strptime(loan_item[2], "%d/%m/%y")+timedelta(days=14), "%d/%m/%y")])
    return loans_list

from sqlite3 import*

def delete_book(conn, title, author):
    cursor=conn.cursor()
    cursor.execute("""SELECT books.id, loans.id, holds.id FROM books 
                   LEFT JOIN holds ON books.id=holds.book_id 
                   LEFT JOIN loans ON books.id = loans.book_id 
                   WHERE title=? AND author=?""", (title, author))
    id_1=cursor.fetchall()
    if not id_1:
        print('Нельзя удалить книгу, ее нет в библиотеке')
        return False
    id_1=id_1[0]
    holds_id=id_1[1]
    loans_id=id_1[2]
    if loans_id:
        print("нельзя удалить книгу: она выдана")
        return False
    if holds_id:
        print("нельзя удалить книгу: она забронирована")
        return False
    cursor.execute("""DELETE FROM books WHERE title=? AND author=?""", (title, author))
    print(f'книга {title} удалена')
    conn.commit()
    return True


def delete_reader(conn, pr):
    cursor=conn.cursor()
    cursor.execute("""SELECT id FROM loans WHERE pr=?""", (pr,))    
    loans_id=cursor.fetchone()
    if loans_id:
        print("нельзя удалить читателя, у него на руках книги")
        return False
    cursor.execute("""SELECT id FROM holds WHERE pr=?""", (pr,))    
    holds_id=cursor.fetchone()
    if holds_id:
        print("нельзя удалить читателя, у него есть брони")
        return False
    cursor.execute("""DELETE FROM readers WHERE pr=?""", (pr,))
    conn.commit()
    return True

def add_reader(conn, full_name, phone, age):
    cursor=conn.cursor()
    first_name=full_name.split()[0]
    last_name=full_name.split()[1]
    pr=f'{first_name[0]}{last_name[0]}{len(first_name)}{len(last_name)}{phone[-4:]}'
    cursor.execute("""INSERT INTO readers (pr, full_name, phone, age) VALUES (?, ?, ?, ?)""", (pr, full_name, phone, age))
    conn.commit()
    return True
    
def add_book(conn, title, author, genre, n):
    cursor=conn.cursor()
    cursor.execute("""SELECT id, total, free FROM books WHERE title=? AND author=?""", (title, author))
    book_item=cursor.fetchone()
    if book_item:
        book_id=book_item[0]
        cur_total=book_item[1]
        cur_free=book_item[2]
        cursor.execute("""UPDATE books SET total = ?, free=? WHERE id=? """, (cur_total+n, cur_free+n, book_id))
        conn.commit()
        return True
    cursor.execute("""INSERT INTO books (title, author, genre, total, free) VALUES (?, ?, ?, ?, ?)""", ( title, author, genre, n, n))
    conn.commit()
    return True
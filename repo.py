from sqlite3 import*

def delete_book(conn, title, author):
    cursor=conn.cursor()
    cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    id_1=cursor.fetchone()
    if not id_1:
        print('Нельзя удалить книгу, ее нет в библиотеке')
        return False
    id_1=id_1[0]
    cursor.execute("""SELECT id FROM loans WHERE id=?""", (id_1,))
    loans_id=cursor.fetchone()
    if loans_id:
        print("нельзя удалить книгу: она выдана")
        return False
    cursor.execute("""SELECT id FROM holds WHERE id=?""", (id_1,))
    holds_id=cursor.fetchone()
    if holds_id:
        print("нельзя удалить книгу: она забронирована")
        return False
    cursor.execute(f"""DELETE FROM books WHERE id = {id_1}""")
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
    cursor.execute("""SELECT id FROM books WHERE title=? AND author=?""", (title, author))
    book_id=cursor.fetchone()
    if book_id:
        cursor.execute("""SELECT total FROM books WHERE id=?""", (book_id[0]))
        cur_total=cursor.fetchone()[0]
        cursor.execute("""UPDATE books WHERE id=? SET total = ?""", (book_id[0], cur_total+n))
        conn.commit()
        return True
    cursor.execute("""SELECT MAX(id) FROM books""")
    max_id=cursor.fetchone()[0]
    if not max_id:
        max_id=0
    cursor.execute("""INSERT INTO books (id, title, author, genre, total, free) VALUES (?, ?, ?, ?, ?, ?)""", (max_id+1, title, author, genre, n, n))
    conn.commit()
    return True

from sqlite3 import*

def delete_book(conn, title, author):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM books WHERE title=? AND author=?''', 
                   (title, author))
    id_1=cursor.fetchone()[0]
    cursor.execute('''SELECT id FROM loans WHERE id=?''',
                   (id_1))
    loans_id=cursor.fetchone()
    if loans_id:
        print("нельзя удалить книгу: она выдана")
        return False
    cursor.execute('''SELECT id FROM holds WHERE id=?''',
            (id_1))
    holds_id=cursor.fetchone()
    if holds_id:
        print("нельзя удалить книгу: она забронирована")
        return False
    cursor.execute(f'''DELETE FROM books WHERE id = {id_1}''')
    conn.commit()
    print(f'книга {title} удалена')
    return True


def delete_reader(conn, pr):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM loans WHERE pr=?''',
                   (pr))    
    loans_id=cursor.fetchone()
    if loans_id:
        print("нельзя удалить читателя, у него на руках книги")
        return False
    cursor.execute('''SELECT id FROM holds WHERE pr=?''',
                   (pr))    
    holds_id=cursor.fetchone()
    if holds_id:
        print("нельзя удалить читателя, у него есть брони")
        return False
    cursor.execute('''DELETE FROM readers WHERE pr=?''',
                   (pr))
    return True

def add_reader(conn, full_name, phone, age):
    cursor=conn.cursor()
    first_name=full_name.split()[0]
    last_name=full_name.split()[1]
    pr=f'{first_name[0]}{last_name[0]}{len(first_name)}{len(last_name)}{phone[6:]}'
    cursor.execute('''INSERT INTO readers VALUES pr=?, full_name=?, phone=?, age=?''',
                   (pr, full_name, phone, age))
    return True
    
def add_book(conn, title, author, genre, n):
    cursor=conn.cursor()
    cursor.execute('''SELECT id FROM books WHERE title=?, author=?''',
                   (title, author))
    book_id=cursor.fetchone()[0]
    if book_id:
        cursor.execute('''SELECT total FROM books WHERE id=?''',
                       (book_id))
        cur_total=cursor.fetchone()[0]
        cursor.execute('''UPDATE books WHERE id=? SET total = ?''',
                       (book_id, cur_total+n))
        return True
    cursor.execute('''INSERT INTO books VALUES id=? title=?, author=?, genre=?, total=?, free=?''',
                   (book_id, title, author, genre, n, n))
    return True
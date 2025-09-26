from sqlite3 import*
conn=connect('project666.db') 
cursor=conn.cursor()
def delete_book():
    id_1=int(input('введите id '))
    cursor.execute("SELECT books.id FROM books JOIN loans book_id.id=books.id")
    loans_id=cursor.fetchall()
    if id_1 in loans_id:
        print("Вы не можете удалить эту книгу")
    else:
        cursor.execute("DELETE FROM books WHERE id = id_1")

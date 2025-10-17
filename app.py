#тест функций
from repo import*
from service import*
from sqlite3 import*
conn=connect('project666.db')
add_book(conn, 'book_4', 'author_4', 'fantastic', 1)
cursor=conn.cursor()
cursor.execute('''SELECT * FROM books''')
print(cursor.fetchall())

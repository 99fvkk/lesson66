from repo import*
from service import*
from project6 import*
db_connect=connection()
db_cursor=db_connect.cursor()
#delete_book(db_connect, title, author)
#delete_reader(db_connect, "ВЯ430725")
#add_reader(db_connect, "Ваху Яки", "+79652050725", 67)
#add_book(db_connect, "book 9", "author 9", "fantasy", 5)
#borrow_book(db_connect, "ИИ462233", "book_1", "author_1")
#cancel_hold(db_connect, "ИИ462233", "book 66", "author 66")
#hold_book(db_connect, "ИИ462233", "book_4", "author_4")
#print(return_holds(db_connect, "ИИ462233"))
#print(return_loans(db_connect, "ИИ462233"))
#db_cursor.execute("""SELECT * FROM holds""")
#print(db_cursor.fetchall())

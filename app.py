from repo import*
from service import*
from project6 import*


find_book(db_connect, "book_1", author=None, genre=None)
print(db_cursor.fetchall())


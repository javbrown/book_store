from book import *

class BookRepo:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM books')
        books = []
        for row in rows:
            item = Book(row['title'], row['author'], row['id'])
            books.append(item)
        return books
    def create(self, book):
        return self._connection.execute('INSERT INTO books (title, author) VALUES (%s, %s)', [book.title, book.author])

    def delete(self, book_id):
        return self._connection.execute('DELETE FROM books WHERE id = %s', [book_id])
    
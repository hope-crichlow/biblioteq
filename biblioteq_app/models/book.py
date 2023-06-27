from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash
from biblioteq_app.models import  user


class Book:
    def __init__(self, data):
        self.id = data['book_id']
        self.title = data['title']
        self.author = data['author']
        self.isbn = data['isbn']
        self.due_date = data['due_date']
        self.is_returned = data['is_returned']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.user = None
        
    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, author, isbn, due_date, is_returned, user_id, created_at, updated_at) VALUES (%(title)s, %(author)s, %(isbn)s, NOW(),  %(is_returned)s, %(user_id)s,  NOW(), NOW());"

        return connectToMySQL('book_buddy').query_db(query, data)

    @classmethod
    def get_all_for_dashboard(cls):
        query = "SELECT * FROM books;"

        results = connectToMySQL('book_buddy').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        
        return books

    @classmethod
    def get_one_book(cls, data):
        query = "SELECT * FROM books WHERE books.book_id = %(id)s;"

        results = connectToMySQL('book_buddy').query_db(query, data)
        print('/////////', results)

        book = cls(results[0])

        return book

    @classmethod
    def delete_book(cls, data):

        query = "DELETE FROM books WHERE book_id = %(id)s;"
        connectToMySQL('book_buddy').query_db(query, data)
        
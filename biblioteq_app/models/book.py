from belt_app.config.mysqlconnection import connectToMySQL
from flask import flash
from belt_app.models import author, user, review


class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.user_id = data['user_id']
        self.author_id = data['author_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.reviews = []
        self.author = None
        self.user = None

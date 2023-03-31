from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from biblioteq_app import app



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.address_id = data['address_id']
        self.rate = data['rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.reviews = []
        self.rate = None
        self.address_id = None

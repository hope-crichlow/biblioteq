from biblioteq_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash, session
from biblioteq_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

NAMES_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

db = 'book_buddy'


class Driver:
    def __init__(self, data):
        self.driver_id = data['driver_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.address_id = data['address_id']
        self.rate = data['rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # self.reviews = []
        # self.rate = None
        # self.address_id = None

    @classmethod
    def is_email_unique(cls, data):
        query = "SELECT * FROM drivers WHERE email = %(email)s;"

        results = connectToMySQL('db').query_db(query, data)
        return len(results) == 0

    @classmethod
    def driver_in_db(cls, data):
        query = "SELECT * FROM drivers WHERE email = %(email)s;"

        results = connectToMySQL('db').query_db(query, data)
        if len(results) == 0:
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_logged_in_driver(cls, data):
        query = "SELECT * FROM drivers WHERE driver_id = %(id)s;"

        results = connectToMySQL('db').query_db(query, data)

        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO drivers (first_name, last_name, email, phone_number, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone_number)s, %(pw_hash)s, NOW(), NOW());"

        return connectToMySQL('db').query_db(query, data)

    @staticmethod
    def validate_reg(driver):
        is_valid = True

        if len(driver['first_name']) == 0:
            flash('First Name is required', 'first_name')
            is_valid = False
        elif len(driver['first_name']) < 2:
            flash('First Name must be at least 2 characters', 'first_name')
            is_valid = False
        elif not NAMES_REGEX.match(driver['first_name']):
            flash(
                'First Name must only contain characters from the alphabet', 'first_name')
            is_valid = False

        if len(driver['last_name']) == 0:
            flash('Last Name is required', 'last_name')
            is_valid = False
        elif len(driver['last_name']) < 2:
            flash('Last Name must be at least 2 characters', 'last_name')
            is_valid = False
        elif not NAMES_REGEX.match(driver['last_name']):
            flash('Last Name must only contain characters from the alphabet', 'last_name')
            is_valid = False

        if len(driver['email']) == 0:
            flash('Email is required', 'email')
            is_valid = False
        elif not EMAIL_REGEX.match(driver['email']):
            flash(
                'Invalid email format, must contain @ and . like somedrivername@domain.com', 'email')
            is_valid = False
        elif not Driver.is_email_unique(driver):
            flash('You have already registered with that email, please log in', 'email')
            is_valid = False

        if len(driver['phone_number']) == 0:
            flash('phone number is required', 'phone_number')
            is_valid = False
        elif len(driver['phone_number']) < 10:
            flash('Phone Number must be at least 10 characters', 'phone_number')
            is_valid = False
        elif not PHONE_REGEX.match(driver['phone_number']):
            flash(
                'Invalid phone number format, must contain - like xxx-xxx-xxxx', 'phone_number')
            is_valid = False

        if len(driver['password']) == 0:
            flash('Password is required', 'password')
            is_valid = False
        elif len(driver['password']) < 8:
            flash('Password must be at least 8 characters in length', 'password')
            is_valid = False
        elif driver['password'] != driver['confirm_password']:
            flash('Password must match your Confirm Password', 'password')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_log(log_driver):
        driver_in_db = Driver.driver_in_db(log_driver)

        if not driver_in_db:
            flash('Invalid email/password')
            return False

        if not bcrypt.check_password_hash(driver_in_db.password, log_driver['password']):
            flash('Invalid email/password')
            return False

        return driver_in_db.driver_id
    
    
    @classmethod
    def get_all_drivers(cls):
        query = "SELECT * FROM drivers;"

        results = connectToMySQL('book_buddy').query_db(query)
        drivers = []
        for driver in results:
            drivers.append(cls(driver))
        
        return drivers
    
    @classmethod
    def get_one_driver(cls, data):
        query = "SELECT * FROM drivers WHERE drivers.driver_id = %(id)s;"

        results = connectToMySQL('book_buddy').query_db(query, data)
        print('/////////', results)

        driver = cls(results[0])

        return driver

    @classmethod
    def delete_driver(cls, data):

        query = "DELETE FROM drivers WHERE driver_id = %(id)s;"
        connectToMySQL('book_buddy').query_db(query, data)

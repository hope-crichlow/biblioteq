from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash
from biblioteq_app.models.return_request_item import Return_request_item
from biblioteq_app.models.user import User


class Request:
    def __init__(self, data):
        self.id = data["book_return_request_id"]
        self.user_id = data["user_id"]
        self.assigned_driver_id = data["assigned_driver_id"]
        self.library_id = data["library_id"]
        self.pickup_address_id = data["pickup_address_id"]
        self.special_notes = data["special_notes"]
        self.request_date = data["request_date"]
        self.delivery_fee = data["delivery_fee"]
        self.requested_return_date = data["requested_return_date"]
        self.is_accepted = data["is_accepted"]
        self.is_in_transit = data["is_in_transit"]
        self.is_complete = data["is_complete"]
        self.user_driver_rating = data["user_driver_rating"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.return_request_items = []
        self.assigned_driver_id = None
        self.is_accepted = 0
        self.is_in_transit = 0
        self.is_complete = 0
        self.user_driver_rating = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO book_return_requests (user_id, assigned_driver_id, library_id, pickup_address_id, special_notes, delivery_fee, requested_return_date, created_at, updated_at) VALUES (%(user_id)s, %(assigned_driver_id)s, %(library_id)s, %(pickup_address_id)s, %(special_notes)s, %(delivery_fee)s,%(requested_return_date)s, NOW(), NOW());"

        result = connectToMySQL("book_buddy").query_db(query, data)
        return result

    @classmethod
    def get_all_for_user(cls, data):
        query = "SELECT * FROM book_return_requests WHERE book_return_requests.user_id = %(id)s;"

        results = connectToMySQL("book_buddy").query_db(query, data)
        requests = []
        for request in results:
            requests.append(cls(request))

        return requests

    @classmethod
    def get_one_request(cls, data):
        query = "SELECT * FROM book_return_requests WHERE book_return_requests.book_return_request_id = %(id)s;"

        results = connectToMySQL("book_buddy").query_db(query, data)
        print("/////////", results)

        request = cls(results[0])
        request.return_request_items = Return_request_item.select_all_by_return_request_id(data)

        return request

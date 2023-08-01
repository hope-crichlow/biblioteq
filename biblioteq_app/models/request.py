from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash
from biblioteq_app.models import user


class Request:
    def __init__(self, data):
        self.id = data["book_return_requests_id"]
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

        self.is_accepted = 0
        self.is_in_transit = 0
        self.is_complete = 0
        self.user_driver_rating = None

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT r.book_return_request_id, r.user_id, r.assigned_driver_id, r.library_id, r.pickup_address_id, r.special_notes, r.request_date, r.delivery_fee, r.requested_return_date, r.is_accepted, r.is_in_transit, r.is_complete, r.user_driver_rating, r.created_at, r.updated_at FROM book_return_requests as r WHERE r.user_id = %(user_id)s;"

    #     results = connectToMySQL('book_buddy').query_db(query)
    #     print('************************', results)
    #     requests = []
    #     for request in results:
    #         requests.append(cls(request))
    #     return requests


from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash
from biblioteq_app.models import user


class Address:
    def __init__(self, data):
        self.id = data["address_id"]
        self.street_address_1 = data["street_address_1"]
        self.street_address_2 = data["street_address_2"]
        self.city = data["city"]
        self.region = data["region"]
        self.postal_code = data["postal_code"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all_addresses(cls):
        query = "SELECT * FROM addresses;"

        results = connectToMySQL("book_buddy").query_db(query)
        print("///addresses//////", results)
        addresses = []
        for address in results:
            addresses.append(cls(address))

        return addresses

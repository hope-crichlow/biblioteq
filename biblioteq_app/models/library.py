
from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash
from biblioteq_app.models import user


class Library:
    all_libraries= []
    
    def __init__(self, data):
        self.id = data["library_id"]
        self.name = data["name"]
        self.system = data["system"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
        Library.all_libraries.append(self)

    @classmethod
    def get_all_libraries(cls):
        query = "SELECT * FROM libraries;"

        results = connectToMySQL("book_buddy").query_db(query)
        print("///libraries//////", results)
        libraries = []
        for library in results:
            libraries.append(cls(library))

        return libraries

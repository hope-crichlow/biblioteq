from biblioteq_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Return_request_item:
  def __init__(self, data):
    self.id = data["return_request_item_id"],
    self.id = data["book_return_request_id"],
    self.id = data["user_book_id"],
    self.id = data["quantity"],
    self.created_at = data["created_at"],
    self.updated_at = data["updated_at"]
    
  @classmethod
  def save(cls, data):
      query = "INSERT INTO return_request_items (book_return_request_id, user_book_id, quantity, created_at, updated_at) VALUES (%(book_return_request_id)s, %(user_book_id)s, %(quantity)s NOW(), NOW());"

      result = connectToMySQL("book_buddy").query_db(query, data)
      return result
    
  @classmethod
  def select_all_by_return_request_id(cls, data):
      query = "SELECT * FROM return_request_items WHERE return_request_items.book_return_request_id = %(id)s;"

      results = connectToMySQL("book_buddy").query_db(query, data)
      items = []
      for request in results:
          items.append(cls(request))

      return items
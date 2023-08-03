from biblioteq_app import app
from biblioteq_app.controllers import users, books,drivers

if __name__ == "__main__":
    app.run(debug=True)

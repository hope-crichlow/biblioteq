from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User


@app.route('/books/add')
def add_book():
    if not 'user_id' in session:
        return redirect('/')


    return render_template('add_book.html')


@app.route('/books/add', methods=['POST'])
def create_book():
    if not 'user_id' in session:
        return redirect('/')

    data = {
        "title": request.form["title"],
        "author_id": 0,
        "user_id": session["user_id"]
    }



    new_book_id = Book.save(data)
    review_data["book_id"] = new_book_id

    Review.save(review_data)

    return redirect(f'/books/{new_book_id}')

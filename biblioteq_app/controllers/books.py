from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.address import Address
from biblioteq_app.models.user import User
from biblioteq_app.models.book import Book
from biblioteq_app.models.request import Request
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.library import Library


@app.route('/books')
def bookshelf():
    if not 'user_id' in session:
        return redirect('/')


    books = Book.get_all_for_dashboard()
    user = User.get_logged_in_user()
    print(books)
    return render_template('bookshelf.html', books=books, user=user)



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
        "author": request.form["author"],
        "isbn": request.form["isbn"],
        "due_date": request.form["due_date"],
        "is_returned": request.form["is_returned"],
        "user_id": session["user_id"]
    }


    print('****************')
    print(data)
    new_book_id = Book.save(data)


    return redirect(f'/books/{new_book_id}')

@app.route('/books/<int:book_id>')
def one_book(book_id):
    if not 'user_id' in session:
        return redirect('/')

    user = User.get_logged_in_user()
    book_to_display = Book.get_one_book({ "id": book_id })

    if not book_to_display:
        return redirect('/books')
    
    return render_template('one_book.html', book=book_to_display, user=user)


@app.route('/books/<int:book_id>/delete')
def delete_book(book_id):
    if not 'user_id' in session:
        return redirect('/books')

    Book.delete_book({ "id": book_id })
    return redirect('/books')
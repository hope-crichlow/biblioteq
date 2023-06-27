from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User
from biblioteq_app.models.book import Book
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_logged_in_user()
    books = Book.get_all_for_dashboard()
    return render_template('dashboard.html', user=user, books=books)

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_reg(request.form):
        return redirect('/')

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "password": bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
    }

    session['user_id'] = User.save(data)
    return redirect('/dashboard')

@app.errorhandler(404)
def no_response(not_assigned):
    return '404- there is no page here. Go to HOME page'


@app.route('/login', methods=['POST'])
def login():
    user_in_db = User.validate_log(request.form)

    if not user_in_db:
        return redirect('/')

    session['user_id'] = user_in_db
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

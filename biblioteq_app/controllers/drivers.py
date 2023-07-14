from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.book import Book
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/driver_dashboard')
def dashboard():
    if not 'driver_id' in session:
        return redirect('/')
    data = {
        'id': session['driver_id']
    }
    driver = Driver.get_logged_in_driver()
    return render_template('driver_dashboard.html', driver=driver)

@app.route('/driver/register', methods=['POST'])
def register():
    if not Driver.validate_reg(request.form):
        return redirect('/')

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "password": bcrypt.generate_password_hash(request.form["password"]).decode('utf-8'),
        "address_id": None,
        "rate": 0.00
    }

    session['driver_id'] = Driver.save(data)
    return redirect('/driver_dashboard')

# @app.errorhandler(404)
# def no_response(not_assigned):
#     return '404- there is no page here. Go to HOME page'


@app.route('/driver/login', methods=['POST'])
def login():
    driver_in_db = Driver.validate_log(request.form)

    if not driver_in_db:
        return redirect('/')

    session['driver_id'] = driver_in_db
    return redirect('/driver_dashboard')



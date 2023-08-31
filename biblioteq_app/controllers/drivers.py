from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.book import Book
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# @app.route("/")
# def index():
#     return render_template("index.html")


@app.route("/driver_dashboard")
def driver_dashboard():
    if "driver_id" not in session:
        return redirect("/")
    data = {"id": session["driver_id"]}
    driver = Driver.get_logged_in_driver(data)
    return render_template("driver_dashboard.html", driver=driver)


@app.route("/driver/register", methods=["POST"])
def driver_register():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
        # "address_id": None,
        # "rate": 0.00,
    }
    valid = Driver.validate_reg(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form["password"]).decode(
            "utf-8"
        )
        data["pw_hash"] = pw_hash
        driver = Driver.save(data)
        session["driver_id"] = driver

        return redirect("/driver_dashboard")
    return redirect("/")


@app.route("/driver/login", methods=["POST"])
def driver_login():
    driver_in_db = Driver.validate_log(request.form)

    if not driver_in_db:
        return redirect("/")

    session["driver_id"] = driver_in_db
    return redirect("/driver_dashboard")

@app.route('/drivers')
def drivers():
    if not 'user_id' in session:
        return redirect('/')
    
    drivers = Driver.get_all_drivers()
    user = User.get_logged_in_user()
    print(drivers)
    return render_template('drivers.html', drivers=drivers, user=user)

@app.route('/drivers/<int:driver_id>')
def one_driver(driver_id):
    if not 'user_id' in session:
        return redirect('/')

    user = User.get_logged_in_user()
    driver_to_display = Driver.get_one_driver({ "id": driver_id })

    if not driver_to_display:
        return redirect('/drivers')
    
    return render_template('one_driver.html', driver=driver_to_display, user=user)


from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.book import Book
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/driver_dashboard")
def dashboard():
    if "driver_id" not in session:
        return redirect("/")
    data = {"id": session["driver_id"]}
    driver = Driver.get_logged_in_driver(data)
    return render_template("driver_dashboard.html", driver=driver)


@app.route("/driver/register", methods=["POST"])
def register():
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
def login():
    driver_in_db = Driver.validate_log(request.form)

    if not driver_in_db:
        return redirect("/")

    session["driver_id"] = driver_in_db
    return redirect("/driver_dashboard")

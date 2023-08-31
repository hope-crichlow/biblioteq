from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.address import Address
from biblioteq_app.models.library import Library
from biblioteq_app.models.user import User
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.book import Book
from biblioteq_app.models.request import Request
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)


@app.route("/requests")
def request():
    if not "user_id" in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    user = User.get_logged_in_user()
    requests = Request.get_all_for_user(data)
    return render_template("schedule.html", user=user, requests=requests)


@app.route("/requests/new")
def new_request():
    if not "user_id" in session:
        return redirect("/")

    addresses = Address.get_all_addresses()
    libraries = Library.get_all_libraries()
    drivers = Driver.get_all_drivers()
    books = Book.get_all_for_dashboard()
    user = User.get_logged_in_user()
    print(books)
    return render_template(
        "book_return.html",
        books=books,
        user=user,
        drivers=drivers,
        libraries=libraries,
        addresses=addresses,
    )


@app.route("/requests/new", methods=["POST"])
def create_return_request():
    if not "user_id" in session:
        return redirect("/")

    data = {
        "user_id": session["user_id"],
        "assigned_driver_id": request.form["assigned_driver_id"],
        "library_id": request.form["library_id"],
        "pickup_address_id": request.form["pickup_address_id"],
        "special_notes": request.form["special_notes"],
        "delivery_fee": request.form["delivery_fee"],
        "requested_return_date": request.form["requested_return_date"],
    }
    print("data", data)

    new_request_id = Request.save(data)
    return redirect(f"/requests/{new_request_id}")


@app.route("/requests/<int:return_request_id>")
def one_request(return_request_id):
    if not "user_id" in session:
        return redirect("/")

    data = {"id": return_request_id}
    user = User.get_logged_in_user()
    request_to_display = Request.get_one_request(data)
    print("!!!request_to_display", request_to_display)
    if not request_to_display:
        return redirect("/requests")

    return render_template("one_request.html", request=request_to_display, user=user)

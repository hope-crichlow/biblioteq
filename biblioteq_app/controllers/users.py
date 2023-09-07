import os
import pathlib
import requests
from flask import Flask, abort, render_template, redirect, session, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

# from cachecontrol import CacheControl
import google.auth.transport.requests
from biblioteq_app import app
from biblioteq_app.models.user import User
from biblioteq_app.models.book import Book
from biblioteq_app.models.driver import Driver
from biblioteq_app.models.request import Request
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent.parent.parent, "client_secret.json"
)


flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://localhost:5000/callback",
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logins")
def logins():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return (
        f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    )


@app.route("/reader")
def reader():
    return render_template("user_index.html")


@app.route("/reader/account")
def user_account():
    if not "user_id" in session:
        return redirect("/")

    user = User.get_logged_in_user()
    return render_template("view_user.html", user=user)


@app.route("/reader/account/edit")
def edit():
    if not "user_id" in session:
        return redirect("/")

    user = User.get_logged_in_user()
    return render_template("edit_user.html", selected_user=user)


@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user_form(user_id):
    print(user_id)
    # validation needs to be updated to allow for the previous email
    if not User.validate_reg(request.form):
        return redirect("/reader/account/edit")

    data = {
        "user_id": session["user_id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "password": bcrypt.generate_password_hash(request.form["password"]).decode(
            "utf-8"
        ),
    }
    print("************************")
    print(data)
    User.edit(data)
    return redirect("/reader/account")


@app.route("/driver")
def driver():
    return render_template("driver_index.html")


@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    data = {"id": session["user_id"]}
    user = User.get_logged_in_user()
    books = Book.get_all_for_dashboard()
    drivers = (
        Driver.get_all_drivers()
    )  # this will be changed to the first 2 drivers. which 2 tbd
    # requests = Request.get_all()
    requests = Request.get_all_for_user(
        data
    )  # this will be changed to display next 3 instead of all
    return render_template(
        "dashboard.html", user=user, books=books, drivers=drivers, requests=requests
    )


@app.route("/register", methods=["POST"])
def register():
    if not User.validate_reg(request.form):
        return redirect("/")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "phone_number": request.form["phone_number"],
        "password": bcrypt.generate_password_hash(request.form["password"]).decode(
            "utf-8"
        ),
    }

    session["user_id"] = User.save(data)
    return redirect("/dashboard")


@app.errorhandler(404)
def no_response(not_assigned):
    return "404- there is no page here. Go to HOME page"


@app.route("/login", methods=["POST"])
def login():
    user_in_db = User.validate_log(request.form)

    if not user_in_db:
        return redirect("/")

    session["user_id"] = user_in_db
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

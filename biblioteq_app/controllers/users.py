from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def no_response(not_assigned):
  return '404- there is no page here. Go to HOME page'



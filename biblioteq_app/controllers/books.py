from flask import render_template, redirect, session, request
from biblioteq_app import app
from biblioteq_app.models.user import User



# @app.route('/dashboard')
# def dashboard():
#     if not 'user_id' in session:
#         return redirect('/')

#     user = User.get_logged_in_user()

#     return render_template('dashboard.html', user=user)

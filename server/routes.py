from flask import render_template
from server import app, socketio
from markupsafe import escape
from flask_login import login_user, logout_user, login_required, current_user

# A welcome message to test our server
@app.route('/')
def main():
    return "<h1>Welcome to our server!!!!</h1>"


@app.route('/create', methods=['GET', 'POST'])
def emailform():
    return render_template("create.html")

@app.route('/index/<string:email>', methods=['GET', 'POST'])
def index(email):
    return 'Email %s' % escape(email)

@app.route('/afterlogin', methods=['GET', 'POST'])
def afterlogin():
    if current_user.is_authenticated:
        return render_template('afterlogin.html')
    else:
        return 'Your not logged in'
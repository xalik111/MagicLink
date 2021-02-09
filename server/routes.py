from flask import render_template,redirect, url_for
from server import app, socketio
from markupsafe import escape
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import string
import random

from .models import Users

# A welcome message to test our server
@app.route('/')
def main():
    return "<h1>Welcome to our server!!!!</h1>"


@app.route('/create', methods=['GET', 'POST'])
def emailform():
    return render_template("create.html")

@app.route('/index/<string:email>', methods=['GET', 'POST'])
def index(email):
    login = escape(email)
    try:
        user = Users.select().where(Users.login == login).get()
        return render_template('index.html', email=user.login, password=user.password, magiclink=user.magiclink, url_counter=user.url_counter)
    except Exception:
        hash_pwd = generate_password_hash('Qwerty123')
        magiclink = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        Users.create(login=login, password=hash_pwd, magiclink=magiclink, url_counter=0)
        return render_template('index.html', email=login, password=hash_pwd, magiclink=magiclink, url_counter=0)
        #return 'User %s created %s' % (escape(email), magiclink)
    

@app.route('/afterlogin', methods=['GET', 'POST'])
@login_required
def afterlogin():
    if current_user.is_authenticated:
        return render_template('afterlogin.html')
    else:
        return 'You don\'t login'

@app.route('/ml/<string:link>', methods=['GET', 'POST'])
def magic_link(link):
    try:
        user = Users.select().where(Users.magiclink == link).get()
        login_user(user)
        query = user.update(url_counter=user.url_counter+1)
        return str(query)
        """query.execute()
        return redirect(url_for('afterlogin')) """
    except Exception as ex:
        return str(ex)
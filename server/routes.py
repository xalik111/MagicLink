import os
import random
import string

import sendgrid
from flask import redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from markupsafe import escape
from sendgrid.helpers.mail import *
from werkzeug.security import check_password_hash, generate_password_hash

from server import app, socketio

from .models import Users

@app.route('/')
def main():
    return "<h1>Welcome to our server!!!!</h1>"

@app.route('/create', methods=['GET', 'POST'])
def emailform():
    return render_template("create.html")

@app.route('/changestatus', methods=['GET', 'POST'])
def changestatus():
    login =  request.form["email"]
    user = Users.get_or_none(Users.login == login)
    if user is not None:
        if user.is_enable == 'Yes':
            user.is_enable = 'No'
            user.save()
            #change to no
            return redirect(url_for('index'))
        else:
            user.is_enable = 'Yes'
            user.save()
            #change to yes
            return redirect(url_for('index'))
    else:
        return 'wow, don\'t know this user'


@app.route('/index/<string:email>', methods=['GET', 'POST'])
def index(email):
    login = escape(email)
    user = Users.get_or_none(Users.login == login)
    if user is not None:
        return render_template('index.html', email=user.login, password=user.password, magiclink=user.magiclink, url_counter=user.url_counter, is_enable=user.is_enable)
    else:
        try:
            hash_pwd = generate_password_hash('Qwerty123')
            magiclink = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            Users.create(login=login, password=hash_pwd, magiclink=magiclink, url_counter=0, is_enable='Yes')
            sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("xalik@meta.ua")
            to_email = To(str(login))
            subject = "Magic Link"
            content = Content("text/plain", "Your magic link is http://magiclinktest.herokuapp.com/ml/%s" % magiclink)
            mail = Mail(from_email, to_email, subject, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            return render_template('index.html', email=login, password=hash_pwd, magiclink=magiclink, url_counter=0, is_enable='Yes')
        except Exception:
            return 'something went wrong'

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
        if user.is_enable == 'Yes':
            login_user(user)
            count = Users.update(url_counter=user.url_counter+1).where(Users.magiclink == link)
            count.execute()
            return redirect(url_for('afterlogin'))
        else:
            return 'This link is expired'
    except Exception as ex:
        return str(ex)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('afterlogin'))

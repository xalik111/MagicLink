import os
import random
import string

import sendgrid
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from markupsafe import escape
from sendgrid.helpers.mail import *
from werkzeug.security import check_password_hash, generate_password_hash

from server import app, mail, socketio

from .models import Users


# A welcome message to test our server
@app.route('/')
def main():
    return "<h1>Welcome to our server!!!!</h1>"

@app.route("/mail")
def send_mail():
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("xalik@meta.ua")
    to_email = To("xalikxalik44@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return str(response.status_code)


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
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("xalik@meta.ua")
        to_email = To(str(login))
        subject = "Magic Link"
        content = Content("text/plain", "Your magic link is %s" % magiclink)
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
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
        area = Users.update(url_counter=user.url_counter+1).where(Users.magiclink == link)
        area.execute()
        return redirect(url_for('afterlogin'))
    except Exception as ex:
        return str(ex)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('afterlogin'))

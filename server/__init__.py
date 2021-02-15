from flask import Flask, jsonify, render_template_string, request
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO

app = Flask(__name__)
mail= Mail(app)
app.secret_key = 'somesecretsalt'
manager = LoginManager(app)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'xalikxalik44@gmail.com',
    MAIL_PASSWORD = 'Awesomest!(98',
))


from server import models, routes

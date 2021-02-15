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
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xalikxalik44@gmail.com'
app.config['MAIL_PASSWORD'] = 'Awesomest!(98'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


from server import models, routes

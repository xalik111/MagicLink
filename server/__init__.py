from flask import Flask, render_template_string, render_template_string, request, jsonify
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'somesecretsalt'
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

from server import routes, models
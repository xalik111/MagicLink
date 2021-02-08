from flask import render_template
from server import app, socketio


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!!!</h1>"


@app.route('/create', methods=['GET', 'POST'])
def emailform():
    return render_template("create.html")
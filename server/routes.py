from flask import render_template
from server import app, socketio
from markupsafe import escape

# A welcome message to test our server
@app.route('/')
def main():
    return "<h1>Welcome to our server!!!!</h1>"


@app.route('/create', methods=['GET', 'POST'])
def emailform():
    return render_template("create.html")

@app.route('/index/<path:subpath>', methods=['GET', 'POST'])
def index(subpath):
    return 'Subpath %s' % escape(subpath)
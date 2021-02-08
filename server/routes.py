from server import app, socketio


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!!!</h1>"
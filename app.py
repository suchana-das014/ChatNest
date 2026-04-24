from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}  # sid -> nickname

@app.route('/')
def index():
    return render_template('index.html')


# JOIN EVENT
@socketio.on('join')
def handle_join(data):
    nickname = data['nickname']
    users[request.sid] = nickname

    emit('message', {
        'user': 'System',
        'text': f"{nickname} joined the chat"
    }, broadcast=True)


# MESSAGE EVENT
@socketio.on('message')
def handle_message(msg):
    nickname = users.get(request.sid, "Unknown")

    emit('message', {
        'user': nickname,
        'text': msg
    }, broadcast=True)


# DISCONNECT EVENT
@socketio.on('disconnect')
def handle_disconnect():
    nickname = users.get(request.sid, "Unknown")
    users.pop(request.sid, None)

    emit('message', {
        'user': 'System',
        'text': f"{nickname} left the chat"
    }, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import os
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS

log_file_path = os.path.join(os.path.dirname(__file__), 'log_file.log')
last_lines = []

def tail(filename, n=10):
    """Read last n lines from the given file."""
    with open(filename, 'r') as f:
        return ''.join(f.readlines()[-n:])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def get_logs():
    return jsonify(last_lines)

def watch_file():
    global last_lines
    with open(log_file_path, 'r') as f:
        # Move the file pointer to the end
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                last_lines.append(line)
                if len(last_lines) > 10:
                    last_lines.pop(0)  # Keep only the last 10 lines
                socketio.emit('logUpdate', {'data': line})  # Emit the new line
            else:
                time.sleep(0.1)  # Wait for new data to be appended

@socketio.on('connect')
def handle_connect():
    emit('logUpdate', {'data': last_lines})
    thread = Thread(target=watch_file)
    thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
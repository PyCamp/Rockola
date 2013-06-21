
from time import time
from flask import json
from flask import Flask, request
from flask import render_template
from msgs_queue import queue_manager
#from rabbit_sse import sse
#from rabbit_sse import send_event

app = Flask(__name__)
app.debug = True
#app.register_blueprint(sse, url_prefix='/messages')

#shiva = ShivaClient()

qm = queue_manager.Queue()
cmdq = queue_manager.get_queue_name('control')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/songs')
def update_latest_songs():
    """List latest added songs."""
    songs = [
        {'id': 1,
        'title': 'Smoke on the Water',
        'artist': 'Deep Purple',
        },
        {'id': 2,
        'title': 'Faithful',
        'artist': 'Pearl Jam',
        },
        {'id': 3,
        'title': 'No Way',
        'artist': 'Pearl Jam',
        },
        {'id': 4,
        'title': 'Daughter',
        'artist': 'Pearl Jam',
        },
    ]

    data = dict(message=songs)
    #send_event("latest", json.dumps(data), channel='rockola')
    return ""


@app.route('/songs/add')
def add_song():
    """Add a song to be reproduced."""
    return render_template('pong!')


@app.route('/songs/latest')
def list_latest_songs():
    """List latest added songs."""

@app.route('/update_lists')
def update_list():
    lists = json.loads(request.args['data'])
    print lists
    return "ok"

@app.route('/control/newsong')
def new_song():
    """push new song in the player"""

@app.route('/vote')
def vote():
    id_track = request.args['track_id']
    operation = request.args['operation']
    timestamp = int(time())
    id_session = request.remote_addr
    keys = ['id_track', 'operation', 'timestamp', 'id_session']
    values = [id_track, operation, timestamp, id_session]
    data = dict(zip(keys, values))
    msg = json.dumps(data)
    qm.send(cmdq, msg)
    return "ok"

if __name__ == '__main__':
    app.run('0.0.0.0')

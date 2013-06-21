import json
from flask import Flask, request
from flask import json
from flask import url_for
from flask import redirect
from flask import render_template
from flask.ext.sse import sse
from flask.ext.sse import send_event
from player import ShivaClient

app = Flask(__name__)
app.debug = True
app.register_blueprint(sse, url_prefix='/messages')

#shiva = ShivaClient()

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
    send_event("latest", json.dumps(data), channel='rockola')
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


if __name__ == '__main__':
    app.run('0.0.0.0')

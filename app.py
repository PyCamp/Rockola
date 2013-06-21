from flask import Flask
from flask import json
from flask import url_for
from flask import redirect
from flask import render_template
from flask.ext.sse import sse
from flask.ext.sse import send_event

app = Flask(__name__)
app.debug = True
app.register_blueprint(sse, url_prefix='/messages')


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


if __name__ == '__main__':
    app.run('0.0.0.0')

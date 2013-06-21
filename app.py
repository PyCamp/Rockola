from flask import json
from flask import Flask, request
from flask import render_template
from player import ShivaClient, VLCController
from rabbit_sse import sse
from rabbit_sse import send_event

app = Flask(__name__)
app.debug = True
app.register_blueprint(sse, url_prefix='/messages')

shiva = ShivaClient()
vlc = VLCController()

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
    top, last = lists['top'], lists['lasts']

    ids = set([track_id for track_id, _ in top])
    ids |= set(last)

    tracks_info = shiva.get_tracks(ids)

    for i, (track_id, votos) in enumerate(top):
        info = tracks_info[track_id]
        top[i][0] = {'id' : track_id,
                     'title': info['title'],
                     'artist': info['artist']}

    for i, (track_id, votos) in enumerate(last):
        info = tracks_info[track_id]
        last[0] = {'id' : track_id,
                     'title': info['title'],
                     'artist': info['artist']}

    msg_to_ui = {'top': top, 'last': last}
    print msg_to_ui
    #FIXME: Pushear esta info a la UI

    return "ok"

@app.route('/newsong')
def new_song():
    """push new song in the player"""

if __name__ == '__main__':
    app.run('0.0.0.0')

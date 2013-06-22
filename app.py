#!/urs/bin/env python
#-*- coding: utf-8 -*-
from time import time
from flask import json
from flask import Flask, request
from flask import render_template
from msgs_queue import queue_manager
from player import ShivaClient, VLCController
import requests
from msgs_queue.receive_list_process import ReceiveListProcess
app = Flask(__name__)

shiva = ShivaClient()
vlc = VLCController()
rl = ReceiveListProcess()
rl.run()

qm = queue_manager.Queue()
cmdq = queue_manager.get_queue_name('control')
listsq = queue_manager.get_queue_name('lists')

@app.route('/')
def home():
    #msg = None
    #while not msg:
        #msg = qm.receive_no_block(listsq)
    print 'queues empty'
    songs = shiva.get_tracks(short=True)
    return render_template('index.html',
            songs = songs)


@app.route('/songs/add')
def add_song():
    """Add a song to be reproduced."""
    return render_template('pong!')


@app.route('/need_list')
def need_list():
    """List latest added songs."""
    operation = request.args['operation']
    timestamp = int(time())
    id_session = request.remote_addr
    keys = ['operation', 'timestamp', 'id_session']
    values = [operation, timestamp, id_session]
    data = dict(zip(keys, values))
    msg = json.dumps(data)
    qm.send(cmdq, msg)
    return "ok"

@app.route('/update_lists')
def update_list():
    lists = json.loads(request.args['data'])
    top, last = lists['top'], lists['last']

    ids = set([track_id for track_id, _ in top])
    ids |= set([track_id for track_id, _ in last])

    tracks_info = shiva.get_tracks(ids)
    print lists, tracks_info
    def _fill_track_data(tracks):
        response = []
        for track_id, votos in top:
            info = tracks_info[track_id]
            response.append({'id' : track_id,
                             'title': info['title'],
                             'artist': info['artist'],
                             'votes': votos})
        return response

    response = {'top': _fill_track_data(top),
                'last': _fill_track_data(last)}

    payload = {
        "message": json.dumps(response),
        "channel": "base"
    }
    print payload
    r=requests.post("http://localhost:8888/publish", data=payload)


    return "ok"

@app.route('/newsong')
def new_song():
    """push new song in the player"""
    song_id = int(request.args['song_id'])
    track_info = shiva.get_tracks([song_id])[song_id]
    vlc.add_song(track_info['path'])
    return 'ok'


@app.route('/vote')
def vote():
    id_track = int(request.args['track_id'])
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
    app.debug = True
    app.run('0.0.0.0')

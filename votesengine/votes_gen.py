# -*- coding: utf-8 -*-
import queue_manager
import json
import random
import time

from time import sleep

sessions = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
operations = ['votarpositivo', 'votarnegativo']


def generate_votes():
    '''Generates random votes.
       Returns a dict:
           {"id_sesion": "abcdfg",
            "timestamp": 1389289869,
            "id_track": 1827,
            "operation": "votarpositivo"}'''
    vote_dict = {
        'id_sesion': random.choice(sessions),
        'timestamp': time.time(),
        'id_track': int(random.gauss(4, 1))+1,
        'operation': random.choice(operations)}
    return json.dumps(vote_dict)


control_name = queue_manager.get_queue_name('control')
cmd_sender = queue_manager.Queue()

for i in range(60):
    cmd_sender.send(control_name ,generate_votes())
    sleep(1)

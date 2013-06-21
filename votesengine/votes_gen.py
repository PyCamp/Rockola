# -*- coding: utf-8 -*-
import control_queue
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
        'id_track': random.randrange(10),
        'operation': random.choice(operations)}
    return json.dumps(vote_dict)




for i in range(100):
    sender = control_queue.Publisher()
    sender.send_command(generate_votes())
    sleep(1)

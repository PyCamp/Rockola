# -*- coding: utf-8 -*-
import time
import random

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
    return vote_dict

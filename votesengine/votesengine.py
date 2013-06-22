#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import queue_manager
import json
import requests
from random import randint

from time import sleep
URL = "http://localhost:5000/"


def play_new_song(newsong):
    """se usa para avisarle a player que reproduzca una nueva cancion"""
    print {"song_id": newsong}
    requests.get(URL + "newsong", params={"song_id": newsong})
    ##aca va el raise status de request
    #raise NotImplementedError()


class VoteEngine(object):

    def __init__(self, newsongmethod=play_new_song):
        self.status = 'RANDOM'
        self.newsong = newsongmethod
        self.current_votes = votos.VoteManager()
        rand = (randint(1, 50), 1)
        self.random_list = {'top': [rand], 'last': [rand]}
        self.now_playing = -1

    def nuevacancion(self, new_json=None):
        if len(self.current_votes.votos) == 0:
            self.status = 'RANDOM'
            rand = (randint(1, 50), 1)
            self.random_list = {'top': [rand], 'last': [rand]}
            id_, vote = rand
            self._newsong(id_)
        else:
            self.status = 'PLAYLIST'

        return self._devolverlistas()

    def votarpositivo(self, vote):
        return self._votos(vote)

    def votarnegativo(self, vote):
        return self._votos(vote)

    def _votos(self, vote):
        self.status = 'PLAYLIST'
        self.current_votes.add_vote(vote)
        lists = self._devolverlistas()
        id_, vote = lists['top'][0]
        self._newsong(id_)
        return lists

    def necesitolista(self, new_json=None):
        return self._devolverlistas()

    def _devolverlistas(self):
        if self.status == 'RANDOM':
            return self.random_list
        elif self.status == 'PLAYLIST':
            top = self.current_votes.top()
            last = self.current_votes.last()
            return {'top': top, 'last': last}
     
    def _newsong(self, id_):
        if self.now_playing == id_:
            pass
        else:
            self.newsong(id_)
            self.now_playing = id_

def main():
    sleep(6)
    #armamos las conexiones a las colas de entrada y salida
    control_name = queue_manager.get_queue_name('control')
    lists_name = queue_manager.get_queue_name('lists')

    receiver = queue_manager.Queue()

    votesengine = VoteEngine()
    while True:
        #Busca un nuevo voto y lo transforma
        new_vote = receiver.receive(control_name)

        new_data = json.loads(new_vote)
        print 'QUERY: ', new_data
        print 'MODE: ', votesengine.status

        operation = getattr(votesengine, new_data['operation'], None)
        if operation:
            response = operation(new_data)
            print 'ANS: ', response
            receiver.send(lists_name, json.dumps(response))
        else:
            print "Operation Not Implemented" + new_data['operation']

if __name__ == '__main__':
    main()

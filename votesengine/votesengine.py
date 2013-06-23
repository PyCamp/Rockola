#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import queue_manager
import json
import requests
from random import randint

from time import sleep, time
URL = "http://localhost:5000/"


def play_new_song(newsong):
    """se usa para avisarle a player que reproduzca una nueva cancion"""
    print {"song_id" : newsong}
    requests.get(URL + "newsong", params = {"song_id" : newsong})
    ##aca va el raise status de request
    #raise NotImplementedError()


class VoteEngine(object):
    
    def __init__(self, newsongmethod = play_new_song):
        self.status = 'IDLE'
        self.newsong = newsongmethod
        self.current_votes = votos.VoteManager()
        self.random_list = None         

    def nuevacancion(self,new_json= None):
        if len(self.current_votos.votos) == 0:
            self.status = 'RANDOM'
            self.random_list = {'top':[(randint(1,50),1)],'last':[]}
        else:
            self.status = 'PLAYLIST'
        self._devolverlistas()
        
    def votarpositivo(self, vote):
        self._votos(vote) 

    def votarnegativo(self,vote):
        self._votos(vote)        

    def _votos(self,vote):
        self.current_votes.add_vote(vote)
        self._devolverlistas()

    def necesitolista(self, new_json= None):
        self._devolverlistas()

    def _devolverlistas(self):
        if self.status == 'RANDOM':
            return self.random_list()


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

        new_data =  json.loads(new_vote)
        print new_data

        operation = getattr(votesengine, new_data['operation'], None)
        if operation:
            operation(new_data)
        else:
            print "Operation Not Implemented" + new_data['operation']

if __name__ == '__main__':
    main()

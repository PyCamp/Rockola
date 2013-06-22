#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import queue_manager
import json
import requests
<<<<<<< HEAD
from random import randint
=======
import random
>>>>>>> 567ad57f4640453c6061eaf8bcb078013091990a

from time import sleep, time
URL = "http://localhost:5000/"


def play_new_song(newsong):
    """se usa para avisarle a player que reproduzca una nueva cancion"""
    print {"song_id" : newsong}
    requests.get(URL + "newsong", params = {"song_id" : newsong})
    ##aca va el raise status de request
    #raise NotImplementedError()

sleep(6)


#armamos las conexiones a las colas de entrada y salida
control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

receiver = queue_manager.Queue()



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

    def _devolverlistas(self)
        if self.status == 'RANDOM':
            return self.random_list()



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





<<<<<<< HEAD
=======
        #parsea y envia las listas de top y last
        updatedata = {"top": top, "last": ultimos}
        receiver.send(lists_name, json.dumps(updatedata))

    elif "nuevacancion" in new_vote["operation"]:
        #elimina la cancion actual de la lista de canciones
        current_votes.endofsong()
        #recalcula el top y devuelve la primera cancion
        try:
            newsong = current_votes.top()[0][0]
        except IndexError:
            id_ = random.randint(1, 100)
            fake_vote = {'timestamp': time(), 'operation': 'votarpositivo',
                         'id_session': '127.0.0.1', 'id_track': id_}
            current_votes.add_vote(fake_vote)
            newsong = current_votes.top()[0][0]

        #llama a la api de player y le pide una nueva cancion
        play_new_song(newsong)

    if current_votes.new_top():
        current_votes.endofsong(current_votes.head)
        newsong = current_votes.top()[0][0]
        play_new_song(newsong)
        # Busca las 5 canciones mas votadas y las 10 ultimas agregadas
        top = current_votes.top()
        ultimos = current_votes.ultimos()
        #parsea y envia las listas de top y last
        updatedata = {"top": top, "last": ultimos}
        receiver.send(lists_name, json.dumps(updatedata))
>>>>>>> 567ad57f4640453c6061eaf8bcb078013091990a



#¿Almacena cada tanto en un sqlite?

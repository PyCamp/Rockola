#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import queue_manager
import json
import requests

def play_new_song(url, newsong):
    """se usa para avisarle a player que reproduzca una nueva cancion"""
    data = json.dumps({"song_id" : newsong[0]})    
    requests.post(url, data = data)
    ##aca va el raise status de request
    #raise NotImplementedError()


current_votes = votos.VoteManager()

#armamos las conecciones a las colas de entrada y salida
control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

receiver = queue_manager.Queue()


while True:
    #Busca un nuevo voto y lo transforma
    new_vote = receiver.receive(control_name)
    new_vote =  json.loads(new_vote)

    if "votar" in new_vote["operation"]:
        #si la operacion es un voto lo agrega
        current_votes.add_vote(new_vote)
        
        # Busca las 5 canciones mas votas y las 10 ultimas agregadas    
        top = current_votes.top()
        ultimos = current_votes.ultimos()
        
        #parsea y envia las listas de top y last
        receiver.send(lists_name ,json.dumps({"top": top, "last": ultimos}))

    elif "necesitolista" in new_vote["operation"]:
        # Busca las 5 canciones mas votas y las 10 ultimas agregadas    
        top = current_votes.top()
        ultimos = current_votes.ultimos()

        #parsea y envia las listas de top y last
        updatedata = {"top": top, "last": ultimos}
        receiver.send(lists_name ,json.dumps({"top": top, "last": ultimos}))

    elif "nuevacancion" in new_vote["operation"]:
        #elimina la cancion actual de la lista de canciones
        current_votes.endofsong(new_vote["current"])
        
        #recalcula el top y devuelve la primera cancion
        newsong = current_votes.top()[0]

        #llama a la api de player y le pide una nueva cancion
        play_new_song(new_vote["url"],newsong)

    if current_votes.new_top():
        current_votes.endofsong(current_votes.last_head)
        newsong = current_votes.top()[0]
        play_new_song(new_vote["url"],newsong)
    


#¿Almacena cada tanto en un sqlite?

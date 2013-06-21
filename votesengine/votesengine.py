#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import queue_manager
import json
import requests

def play_new_song(url, newsong):
    """se usa para avisarle a shiva que reproduzca una nueva cancion"""
    data = json.dumps({"song_id" : newsong[0]})    
    requests.post(url, data = data)
    ##aca va el raise status de request
    #raise NotImplementedError()


current_votes = votos.VoteManager()

control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

cmd_receiver = queue_manager.Receiver(control_name)
lists_receiver = queue_manager.Receiver(lists_name)

lists_sender = queue_manager.Publisher(lists_name)


# read data from rabbitMQ

# parse json

while True:
    new_vote = cmd_receiver.receive()
    print new_vote
    new_vote =  json.loads(new_vote)
    if "votar" in new_vote["operation"]:
        current_votes.add_vote(new_vote)
        top = current_votes.top()
        ultimos = current_votes.ultimos()
        updatedata = {"top": top, "last": ultimos}
        print updatedata
        lists_sender.send(json.dumps(updatedata))
        # Genera las dos listas Top y last
    elif "necesitolista" in new_vote["operation"]:
        pass
    elif "nuevacancion" in new_vote["operation"]:
        current_votes.endofsong(new_vote["current"])
        newsong = current_votes.top()[0]
        play_new_song(new_vote["url"],newsong)




#¿Almacena cada tanto en un sqlite?

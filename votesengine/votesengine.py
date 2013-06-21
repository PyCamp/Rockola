#!/usr/bin/env python
#-*- coding: utf-8 -*-

import votos
import control_queue


def play_new_song(songid):
    """se usa para avisarle a shiva que reproduzca una nueva cancion"""
    raise NotImplementedError()

reciever = control_queue.Reciever()
current_votes = votos.VoteManager()


# read data from rabbitMQ

# parse json


new_vote = reciever.recieve()

if "votar" in new_vote["operation"]:
    current_votes.add_vote(new_vote)
    top = current_votes.top()
    ultimos = current_votes.ultimos()
    updatedata = {"top": top, "last": ultimos}
    print updatedata
    # Genera las dos listas Top y last
elif "necesitolista" in new_vote["operation"]:
    pass
elif "nuevacancion" in new_vote["operation"]:
    newsong = current_votes.top()[0]
    play_new_song(songid)




#¿Almacena cada tanto en un sqlite?

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
import time
from random import randint

COCIENTE_CAMBIOTEMA = 0.5  # Cambia el tema si tiene 50% negativos

def rellenar(func):
    """ Se asegura de que haya al menos un resultado y que no tire
    errores si no hay votos"""
    def decorador(self):
        if self.votos:
            result = func(self)
        else:
            result = [(randint(1,20),0)]
        return result
    return decorador


class VoteManager(object):
    """ Clase que se encarga de generar las listas de reproducción en
    base a los votos que obtiene del JSON en la función add_votes """
    def __init__(self):
        self.votos = dict()
        self.tracks = list()  # Lista de IDs de track, en orden según aparición
        self.track_timestamp = dict()  # Timestamp con fecha en que se inserta
        self.head = 0

    def add_vote(self, voto):
        """ Regenera el diccionario con la cantidad de votos negativos y
        positivos de cada track_id """
        track_id = voto['id_track']
        sessid = voto['id_session']
        calificacion = voto['operation']
        timestamp = voto['timestamp']
        calificacion = 1 if calificacion == 'votarpositivo' else 0
        if track_id not in self.votos:
            self.votos[track_id] = [set([]), set([])]
            self.tracks.append(track_id)
            self.tracks = self.tracks[-10:]  # Conservo los últimos elementos
            self.track_timestamp[track_id] = timestamp
        lista = self.votos[track_id]
        if sessid in lista[not calificacion]:
            # Si votó por lo contrario, borramos el voto anterior
            lista[not calificacion].remove(sessid)
        lista[calificacion].add(sessid)

    def votes(self):
        """ Retorna un diccionario con la cantidad de votos (puede ser
        negativo) de cada track"""
        dicc = dict()
        for track, lista in self.votos.items():
            dicc[track] = len(lista[1]) - len(lista[0])  # positivos - negativos
        return dicc


    def top(self):
        """ Retorna una lista ordenada con tuplas que contienen el
        track_id y su puntaje """
        top = sorted(self.votes().items(), key=lambda v: v[1], reverse=True)[:5]
        return top

    def last(self):
        """ Retorna una lista de tuplas track/puntaje ordenadas según
        la primera vez que fueron votados """
        votos = self.votes()
        tracks = [(track, votos[track]) for track in self.tracks]
        return tracks[-10:]

    def delete(self, track_id):
        del(self.votos[track_id])
        self.tracks.remove(track_id)
       

    def new_top(self):
        """ Retorna True si se debe cambiar la canción por la cantidad
        de votos negativos, de lo contrario False"""
        try:
            lista = self.votos[self.head]
        except KeyError:
            return True 
        cociente = len(lista[0]) / (len(lista[1])+1)  # negativos/positivos
        if cociente >= COCIENTE_CAMBIOTEMA:
            #self.endofsong()
            #self.head = self.votos()[0][0]
            return True
        else:
            return False

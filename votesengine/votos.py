#!/usr/bin/env python
#-*- coding: utf-8 -*-

COCIENTE_CAMBIOTEMA = 0.5  # Cambia el tema si tiene 25% negativos


class VoteManager(object):
    """ Clase que se encarga de generar las listas de reproducción en
    base a los votos que obtiene del JSON en la función add_votes """
    def __init__(self):
        self.votos = dict()
        self.tracks = list()  # Lista de IDs de track, en orden según aparición
        self.last_head = 0
        self.head = 0  # El track_id que está primero

    def add_vote(self, voto):
        """ Regenera el diccionario con la cantidad de votos negativos y
        positivos de cada track_id """
        track_id = voto['id_track']
        sessid = voto['id_sesion']
        calificacion = voto['operation']
        calificacion = 1 if calificacion == 'votarpositivo' else 0
        if not self.votos.has_key(track_id):
            self.votos[track_id] = [set([]), set([])]
            self.tracks.append(track_id)
            self.tracks = self.tracks[-10:]  # Conservo los últimos elementos
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
        track_id y su cantidad de votos """
        top = sorted(self.votes().items(), key=lambda v: v[1], reverse=True)[:5]
        try:
            self.head = top[0][0]
        except KeyError:
            pass
        return top

    def ultimos(self):
        """ Retorna una lista de tracks ordenadas según la primera vez
        que fueron votados """
        return list(reversed(self.tracks))[:10]

    def endofsong(self, track_id=None):
        """ Elimina la canción más votada de la lista, o la canción
        correspondiente al track_id si es especificado"""
        if track_id is None:
            track_id = self.top()[0][0]
        try:
            del(self.votos[track_id])
        except KeyError:
            pass
        else:
            self.head = self.top()[0][0]

    def new_top(self):
        """ Retorna True si se debe cambiar la canción por la cantidad
        de votos negativos, de lo contrario False"""
        lista = self.votos[self.head]
        cociente = len(lista[0]) / len(lista[1])  # negativos/positivos
        print cociente
        if cociente >= COCIENTE_CAMBIOTEMA:
            #self.endofsong()
            #self.head = self.votos()[0][0]
            return True
        else:
            return False

#!/usr/bin/env python
#-*- coding: utf-8 -*-

class VoteManager(object):
	""" Clase que se encarga de generar las listas de reproducción en
	base a los votos que obtiene del JSON en la función add_votes """
	def __init__(self):
		self.votos = dict()
		self.tracks = list() # Lista de IDs de track, en orden según aparición

	def add_vote(self, voto):
		""" Regenera el diccionario con la cantidad de votos negativos y
		positivos de cada track_id """
		track_id = voto['id_track'] 
		sessid = voto['id_sesion'] 
		calificacion = voto['operation']
		calificacion = 1 if calificacion=='votarpositivo' else 0
		if not self.votos.has_key(track_id):
			self.votos[track_id] = [set([]), set([])]
			self.tracks.append(track_id)
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
			dicc[track] = len(lista[1]) - len(lista[0]) # positivos - negativos
		return dicc

	def top(self):
		""" Retorna una lista ordenada con tuplas que contienen el
		track_id y su cantidad de votos """
		return sorted(self.votes().items(), key=lambda v: v[1], reverse=True)

	def ultimos(self):
		""" Retorna una lista de tracks ordenadas según la primera vez
		que fueron votados """
		return list(reversed(self.tracks))
	

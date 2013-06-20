#!/usr/bin/env python
#-*- coding: utf-8 -*-

class VoteManager(object):
	def add_votes(self, json_dict):
		""" Genera un diccionario con la cantidad de votos negativos y
		positivos de cada track_id """
		votos = {}
		for voto in json_dict:
			track_id = voto['id_track'] 
			sessid = voto['id_sesion'] 
			calificacion = int(voto['vote']) 
			if not votos.has_key(track_id):
				votos[track_id] = [set([]), set([])]
			lista = votos[track_id]
			if sessid in lista[not calificacion]:
				# Si votó por lo contrario, borramos el voto anterior
				lista[not calificacion].remove(sessid)
			lista[calificacion].add(sessid)
		self.votos = votos

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
	

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import random
import time
import votos
import votesengine

def callback(track_id):
    #print 'Está sonando', track_id
    pass

class TestVotesEngine(unittest.TestCase):
    def setUp(self):
        self.engine = votesengine.VoteEngine(callback)
        self.engine.nuevacancion()

    def votar(self, track_id, positivo = True, sessid = None,
            timestamp = None):
        if sessid is None:
            sessid = random.random()
        if timestamp is None:
            timestamp = time.time()
        positivo = 'votarpositivo' if positivo else 'votonegativo'
        func = self.engine.votarpositivo if positivo else self.engine.votarnegativo
        func(dict(
            id_track = track_id,
            timestamp = timestamp,
            operation = positivo,
            id_session = sessid))

    def test_inicial(self):
        """ El modo inicial es IDLE. La canción no es -1 """
        self.assertEquals(self.engine.status, 'RANDOM')
        self.assertNotEquals(self.engine.now_playing, -1)

    def test_nuevacancion(self):
        """ Prueba general de nuevacancion, función que llamada cuando
        se termina de reproducir el tema actual """
        # Se arranca en modo random
        self.engine.nuevacancion()
        self.assertEquals(self.engine.status, 'RANDOM')

        # Suena la canción 5, se pasa a modo playlist
        self.votar(5)
        self.assertEquals(self.engine.status, 'PLAYLIST')
        self.assertEquals(self.engine.now_playing, 5)

        # Termina de sonar la 5, se debe pasar a modo random
        self.engine.nuevacancion()
        self.assertEquals(self.engine.status, 'RANDOM')

    def test_votar_manual(self):
        self.engine._votos(dict(
            id_track = 5,
            id_session = 'aaa',
            timestamp = time.time(),
            operation = 'votarpositivo'
            ))
        self.assertEquals(len(self.engine.current_votes.votos), 1)

    def test_votar_funcion(self):
        self.votar(5)
        self.assertEquals(len(self.engine.current_votes.votos), 1)

    def test_cambiodirecto(self):
        """ Si está en modo random y se vota automáticamente se pasa a
        modo playlist """
        self.votar(2)
        self.assertEquals(self.engine.now_playing, 2)

    def test_top(self):
        for i in range(5): self.votar(1)
        for i in range(15): self.votar(2)
        self.assertEquals(self.engine.status, 'PLAYLIST')
        top = self.engine.necesitolista()['top']
        self.assertEquals(top, [(2, 15), (1, 5)])

    def test_last(self):
        for i in range(1,30):
            self.votar(i)
        self.engine.nuevacancion()
        self.assertEquals(self.engine.status, 'PLAYLIST')
        last = self.engine.necesitolista()['last']
        self.assertEquals(len(last), 20)
        self.assertEquals(last, [(i, 1) for i in range(10, 30)])

    def test_doblecancion(self):
        """ Una canción puede llegar a sonar dos veces si la vuelven
        a votar """
        self.votar(5)
        #self.engine.nuevacancion() # Suena la 5
        self.assertEquals(self.engine.now_playing, 5)

        self.votar(8)
        print self.engine._devolverlistas()['top']
        self.assertEquals(self.engine.now_playing, 5)
        print 342
        self.engine.nuevacancion() # Suena la 8
        self.assertEquals(self.engine.now_playing, 8)

        self.votar(5)
        self.engine.nuevacancion() # Suena la 5 de nuevo
        self.assertEquals(self.engine.now_playing, 5)

    def test_nowplaying(self):
        """ El engine.now_playing debe funcionar correctamente """
        self.engine.nuevacancion()
        self.votar(5)
        self.assertEquals(self.engine.now_playing, 5)

    def test_muchascanciones(self):
        """ Hay votos para 5 canciones diferentes, tendrían que 
        sonar en orden """
        self.votar(999)
        for i in range(1,5):
            for j in range(i):
                self.votar(i)
        self.engine.nuevacancion()
        for i in [5,4,3,2,1]:
             self.assertEquals(self.engine.now_playing, i)
             self.engine.nuevacancion()

    def test_cancionsuperada(self):
        """ Si una canción obtiene más votos de la que se está 
        reproduciendo se pasa a reproducir esta última """
        self.votar(5)
        self.assertEquals(self.engine.now_playing, 5)
        self.votar(6)
        self.votar(6)
        self.assertEquals(self.engine.now_playing, 6)

    def test_cancionnosuperada(self):
        self.votar(5)
        self.votar(8)
        self.assertEquals(self.engine.now_playing, 5)


if __name__ == '__main__':
    unittest.main()

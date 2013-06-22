#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import votos
import random
import time

class TestVotos(unittest.TestCase):
    def instanciar(self):
        """ Instancia un objeto VoteManager """
        self.votos = votos.VoteManager()

    def votar(self, track_id, positivo = True, sessid = None,
            timestamp = None):
        if sessid is None:
            sessid = random.random()
        if timestamp is None:
            timestamp = time.time()
        positivo = 'votarpositivo' if positivo else 'votonegativo'
        self.votos.add_vote(dict(
            id_track = track_id,
            timestamp = timestamp,
            operation = positivo,
            id_session = sessid))

    def test_votar(self):
        """ La función votar debe funcionar correctamente """
        self.instanciar()
        self.votar(1)
        self.assertEquals(self.votos.top(), [(1,1)])

        self.instanciar()
        self.votar(1, False)
        self.assertEquals(self.votos.top(), [(1,-1)])

    def test_sin_votos(self):
        """ Verifica que si no hay canciones para mostrar se muestre
        una aleatoria en el rango de 0 a 20, con 0 votos """
        self.instanciar()
        top = self.votos.top()
        track_id, votos = top[0]
        self.assertTrue(track_id > 0 and track_id <= 20)
        self.assertEquals(votos, 0)

    def test_ultimos(self):
        """ Testea el funcionamiento de la funcón ultimos() """
        self.instanciar()
        for i in range(1,21):
            """
            self.votos.add_vote(dict(
                sessid = '127.0.0.1'
                operation = 'votarpositivo'
                timestamp = time.time()
                id_track = i
                ))
                """
            self.votar(i)
        ultimos = self.votos.ultimos()
        tracks = [track_id for track_id, votos in ultimos]
        self.assertEquals(len(ultimos), 10)
        self.assertEquals(tracks, range(11,21))

    def test_votodoble(self):
        """ Un usuario con el mismo sessid no debe tener un solo voto
        negatio o positivo por canción """
        resultados = (
            ((True, True), 1),
            ((False, False), -1),
            ((False, True), 1),
            ((True, False), -1),
            )
        for args, esperado in resultados:
            self.instanciar()
            for positivo in args: 
                self.votar(1, positivo, sessid = 'a')
            track_id, votos = self.votos.top()[0]
            self.assertEquals(votos, esperado)

    def test_puntaje(self):
        """ Una canción más nueva con menos votos que una vieja puede
        llegar a aparecer primera """
        self.instanciar()
        timestamp_viejo = time.time() - 1000
        timestamp_nuevo = time.time() - 100
        for i in range(1000):
            self.votar(3, timestamp = timestamp_nuevo)
        self.assertEquals(self.votos.head, 3)
        for i in range(20):
            self.votar(1, timestamp = timestamp_viejo)
        for i in range(10):
            self.votar(2, timestamp = timestamp_nuevo)
        top = self.votos.top()
        self.assertEquals(top, [(3, 1000), (2, 10), (1, 20)])

    def test_endofsong(self):
        """ Prueba que una canción se borre eficientemente de la lista
        """
        self.instanciar()
        for i in range(5):
            self.votar(1)
        self.votar(2) 
        self.assertEquals(self.votos.head, 1)
        self.votos.endofsong()
        self.assertTrue(self.votos.head, 2)

    def test_cambiocancion(self):
        """ Si una canción tiene muchos votos negativos debería
        indicarse que tiene que ser cambiada """
        self.instanciar()
        for i in range(5):
            self.votar(1)
        self.assertFalse(self.votos.new_top())
        for i in range(10):
            self.votar(1, positivo = False)
        self.assertTrue(self.votos.new_top)


if __name__ == '__main__':
    unittest.main()

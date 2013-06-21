import control_queue
import lists_queue


cmd_sender = control_queue.Publisher()
lists_sender = lists_queue.Publisher()

cmd_sender.send('Hola Motor de votos!!!')
lists_sender.send('{Mana, Dream, Epica}')

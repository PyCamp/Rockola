import queue_manager

control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

sender = queue_manager.Queue()

sender.send(control_name, 'Hola Motor de votos!!!')
sender.send(lists_name, '{Mana, Dream, Epica}')

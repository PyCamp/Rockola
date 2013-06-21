import queue_manager

control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

cmd_sender = queue_manager.Publisher(control_name)
lists_sender = queue_manager.Publisher(lists_name)

cmd_sender.send('Hola Motor de votos!!!')
lists_sender.send('{Mana, Dream, Epica}')

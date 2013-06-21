import queue_manager

control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

sender = queue_manager.Queue()

sender.declare_queue('hola')
sender.declare_queue('chau')

sender.send('hola', 'Hola Motor de votos!!!')
sender.send('chau', '{Mana, Dream, Epica}')

import queue_manager
import json
#control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

sender = queue_manager.Queue()

#sender.send(control_name, 'Hola Motor de votos!!!')
sender.send(lists_name, json.dumps({'top': [(9, 3), (6, 2), (1, 1), (5, 1), (8, 1), (2, 0), (3, -1), (4, -1), (0, -4), (7, -5)], 'last': [0, 4, 5, 8, 6, 2, 7, 1, 3, 9]}))

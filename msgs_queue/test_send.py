import queue_manager
import json
#control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

sender = queue_manager.Queue()

#sender.send(control_name, 'Hola Motor de votos!!!')
sender.send(lists_name, json.dumps({'top': [(9, 3), (6, 2), (1, 1), (5, 1), (8, 1), (2, 0), (3, -1), (4, -1), (10, -4), (7, -5)], 'last': [(10,1), (4,3), (5,5), (8,-1), (6,5), (2,8), (7,0), (1,9), (3,1), (9,2)]}))

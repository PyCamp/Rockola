import queue_manager

from multiprocessing import Process


control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

receiver = queue_manager.Queue()

receiver.declare_queue('hola')
receiver.declare_queue('chau')


def rec_commands():
    while True:
        print receiver.receive('hola')


def rec_lists():
    while True:
        print receiver.receive('chau')


r1 = Process(target=rec_commands)
r2 = Process(target=rec_lists)
r1.start()
r2.start()
r1.join()
r2.join()

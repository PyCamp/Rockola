import queue_manager

from multiprocessing import Process


cmd_receiver = queue_manager.Receiver(control_name)
lists_receiver = queue_manager.Receiver(lists_name)
print cmd_receiver.receive()
print lists_receiver.receive()


def rec_commands():
    while True:
        print cmd_receiver.receive()


def rec_lists():
    while True:
        print lists_receiver.receive()


r1 = Process(target=rec_commands)
r2 = Process(target=rec_lists)
r1.start()
r2.start()
r1.join()
r2.join()


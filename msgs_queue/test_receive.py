import queue_manager

control_name = queue_manager.get_queue_name('control')
lists_name = queue_manager.get_queue_name('lists')

cmd_receiver = queue_manager.Receiver(control_name)
lists_receiver = queue_manager.Receiver(lists_name)


print cmd_receiver.receive()
print lists_receiver.receive()

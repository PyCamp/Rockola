import lists_queue

lists_receiver = lists_queue.Receiver()


def callback(msg):
    print msg

lists_receiver.start_receiving(callback)

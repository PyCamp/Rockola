
import queue_manager
import urllib
from multiprocessing import Process


class ReceiveListProcess(object):

    URL = 'http://localhost:5000/update_lists'

    def __init__(self):
        self.lists_name = queue_manager.get_queue_name('lists')
        self.running = True
        self.receiver = queue_manager.Queue()

    def receive_loop(self):
        while self.running:
            msg = self.receiver.receive(self.lists_name)
            data = urllib.urlencode({'data': msg})
            urllib.urlopen(self.URL, data)

    def run(self):
        p = Process(target=self.receive_loop)
        p.start()
        p.join()

    def stop(self):
        self.stopping = False

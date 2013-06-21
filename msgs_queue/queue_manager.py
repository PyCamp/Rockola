import pika


def get_queue_name(queue):
    names = {'lists': 'lists_queue', 'control': 'control_queue'}
    return names[queue]


class Publisher(object):

    def __init__(self, name, ip='192.168.10.58'):
        self.name = name
        params = pika.ConnectionParameters(host=ip)
        # We connect to the server in a blocking way.
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

        # We use que queue_declare method to be sure that the queue exists.
        # One can call this method infinite times. Only 1 queue is created.
        self.channel.queue_declare(queue=name)

    def send(self, cmd):
        self.channel.basic_publish(exchange='', routing_key=self.name,
                                   body=cmd)


class Receiver(object):

    def __init__(self, name, ip='192.168.10.58'):
        self.name = name
        params = pika.ConnectionParameters(host=ip)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

    def receive(self):
        method = None
        while not method:
            method, header, body = self.channel.basic_get(self.name)
        self.channel.basic_ack(method.delivery_tag)
        return body

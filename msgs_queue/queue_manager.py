"""
Messaging Queue abstraction layer. It uses a RabbitMQ sever.
"""

import pika


def get_queue_name(queue):
    """
    Gets the name of the desired queue. This method enforces that all the
    publishers and subscribers uses the same queue name.

    :param queue: one of 'lists', 'control'
    :returns: the name of the desired queue.
    """
    names = {'lists': 'lists_queue', 'control': 'control_queue'}
    return names[queue]


class Publisher(object):

    def __init__(self, name, ip='192.168.10.58'):
        """
        Creates a publisher class to a message queue.

        :param name: The name of the desired queue.
        :param ip: The IP of the RabbitMQ server.
        """
        self.name = name
        params = pika.ConnectionParameters(host=ip)
        # We connect to the server in a blocking way.
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

        # We use que queue_declare method to be sure that the queue exists.
        # One can call this method infinite times. Only 1 queue is created.
        self.channel.queue_declare(queue=name)

    def send(self, cmd):
        """
        Send a msg to the queue.

        :param cmd: The msg to send.
        """
        self.channel.basic_publish(exchange='', routing_key=self.name,
                                   body=cmd)


class Receiver(object):

    def __init__(self, name, ip='192.168.10.58'):
        """
        Creates a receiver class to a message queue.

        :param name: The name of the desired queue.
        :param ip: The IP of the RabbitMQ server.
        """
        self.name = name
        params = pika.ConnectionParameters(host=ip)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

    def receive(self):
        """
        Blocking method to receive a message from the queue.

        :param name: The name of the desired queue.
        :param ip: The IP of the RabbitMQ server.
        """
        method = None
        while not method:
            method, header, body = self.channel.basic_get(self.name)
        self.channel.basic_ack(method.delivery_tag)
        return body

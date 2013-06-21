"""
Abstraction module for sending and receiving msgs from
different processes using RabbitMQ as back end.
"""
import pika

NAME = 'control_queue'
SERVER_IP = '192.168.10.58'

CONN_PARAM = pika.ConnectionParameters(host=SERVER_IP)


class Publisher(object):
    def __init__(self):
        # We connect to the server in a blocking way.
        connection = pika.BlockingConnection(CONN_PARAM)
        self.channel = connection.channel()

        # We use que queue_declare method to be sure that the queue exists.
        # One can call this method infinite times. Only 1 queue is created.
        self.channel.queue_declare(queue=NAME)

    def send(self, cmd):
        self.channel.basic_publish(exchange='', routing_key=NAME,
                                   body=cmd)


class Receiver(object):
    def __init__(self):
        connection = pika.BlockingConnection(CONN_PARAM)
        self.channel = connection.channel()

    def receive(self):
        method_frame = None
        while not method_frame:
            method_frame, header_frame, body = self.channel.basic_get(NAME)
        self.channel.basic_ack(method_frame.delivery_tag)
        return body

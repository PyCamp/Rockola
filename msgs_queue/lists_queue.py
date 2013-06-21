"""
Abstraction module for sending and receiving msgs from
different processes using RabbitMQ as back end.
"""
import pika

NAME = 'lists_queue'
SERVER_IP = '192.168.10.58'

CONN_PARAM = pika.ConnectionParameters(host=SERVER_IP)


# TODO: Avoid code duplication!!!!
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

    def _callback(self, channel, method_frame, header_frame, body):
        self.callback(body)
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def start_receiving(self, callback):
        self.callback = callback
        self.channel.basic_consume(self._callback, NAME)
        self.channel.start_consuming()

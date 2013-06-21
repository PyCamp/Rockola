import queue_manager
from sse import Sse as PySse
from flask import json, current_app, Blueprint


rabbit_sse = Blueprint('rabbitsse', __name__)
sender = receiver = queue_manager.Queue()
flask_queue = 'flask'  # rabbitmq queue name


class SseStream(object):

    def __iter__(self):
        sse = PySse()
        for data in sse:
            yield data
        for message in receiver.receive(flask_queue):
            if message['type'] == 'message':
                event, data = json.loads(message['data'])
                sse.add_message(event, data)
                for data in sse:
                    yield data


def send_event(event_name, data):
    sender.send(flask_queue, json.dumps([event_name, data]))


@rabbit_sse.route('')
def stream():
    return current_app.response_class(
        SseStream(),
        direct_passthrough=True,
        mimetype='text/event-stream',
    )



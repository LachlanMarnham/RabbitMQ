import json

import random
from time import sleep

import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection


class RabbitBase:
    host = 'localhost'
    port = 5672
    connection_parameters = None

    def __init__(self):
        self._connection_parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
        )
        self._connection = self._get_connection()
        self._channel = self._get_channel()

    def _get_connection(self) -> BlockingConnection:
        return pika.BlockingConnection(self.connection_parameters)

    def _get_channel(self) -> BlockingChannel:
        return self._connection.channel()

    def close(self):
        self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        print('Closing connection!')


class Producer(RabbitBase):

    def __init__(self, queue: str) -> None:
        super().__init__()
        self._exchange = ''
        self._channel.queue_declare(queue)
        self._queue = queue
        self._index = 0

    def publish(self, body: str) -> None:
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._queue,
            body=body,
        )

    def _make_body(self):
        body = {
            'index': self._index,
            'lag': random.randint(1,3),
        }
        self._index += 1
        return json.dumps(body)

    def send(self) -> None:
        body = self._make_body()
        self.publish(body)
        print('sent {}'.format(body))


if __name__ == '__main__':
    with Producer('hello') as producer:
        while True:
            sleep(1)
            producer.send()

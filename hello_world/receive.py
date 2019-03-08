import json
from time import sleep

from send import RabbitBase


class Consumer(RabbitBase):

    def __init__(self, queue: str) -> None:
        super().__init__()
        self._channel.queue_declare(queue)
        self._queue = queue
        self._register_callback()

    @staticmethod
    def callback(ch, method, properties, body):
        body_dict = json.loads(body)
        sleep(body_dict['lag'])
        print('Received {}'.format(body_dict['index']))

    def _register_callback(self):
        self._channel.basic_consume(
            self.callback,
            queue=self._queue,
            no_ack=True,
        )

    def run(self):
        self._channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer('hello')
    consumer.run()

import json
from time import sleep

from send import RabbitBase


class Consumer(RabbitBase):

    def __init__(self, queue: str) -> None:
        super().__init__()
        self._channel.queue_declare(
            queue,
            durable=True,
        )
        self._queue = queue
        self._channel.basic_qos(prefetch_count=1)
        self._register_callback()

    @staticmethod
    def callback(ch, method, properties, body):
        body_dict = json.loads(body)
        sleep(body_dict['lag'])
        print('Received {}'.format(body_dict['index']))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _register_callback(self):
        self._channel.basic_consume(
            self.callback,
            queue=self._queue,
        )

    def run(self):
        self._channel.start_consuming()


if __name__ == '__main__':
    consumer = Consumer('task_queue')
    consumer.run()

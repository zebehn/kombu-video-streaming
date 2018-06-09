"""Kombu-based Video Stream Consumer

Written by Minsu Jang (minsu@etri.re.kr)
Date: 2018-06-09

Reference
- Building Robust RabbitMQ Consumers With Python and Kombu: Part 1 (https://medium.com/python-pandemonium/building-robust-rabbitmq-consumers-with-python-and-kombu-part-1-ccd660d17271)
- Building Robust RabbitMQ Consumers With Python and Kombu: Part 1 (https://medium.com/python-pandemonium/building-robust-rabbitmq-consumers-with-python-and-kombu-part-2-e9505f56e12e)
"""

import cv2
import numpy as np
import sys
import time

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

# Default RabbitMQ server URI
rabbit_url = 'amqp://guest:guest@localhost:5672//'

# Kombu Message Consuming Worker
class Worker(ConsumerMixin):
    def __init__(self, connection, queues):
        self.connection = connection
        self.queues = queues

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queues,
                         callbacks=[self.on_message],
                         accept=['image/jpeg'])]

    def on_message(self, body, message):
        # get the original jpeg byte array size
        size = sys.getsizeof(body.tobytes()) - 33
        # jpeg-encoded byte array into numpy array
        np_array = np.frombuffer(body.tobytes(), dtype=np.uint8)
        np_array = np_array.reshape((size, 1))
        # decode jpeg-encoded numpy array 
        image = cv2.imdecode(np_array, 1)

        # show image
        cv2.imshow("image", image)
        cv2.waitKey(1)

        # send message ack
        message.ack()

def run():
    exchange = Exchange("video-exchange", type="direct")
    queues = [Queue("video-queue", exchange, routing_key="video")]
    with Connection(rabbit_url, heartbeat=4) as conn:
            worker = Worker(conn, queues)
            worker.run()

if __name__ == "__main__":
    run()
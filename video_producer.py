"""Kombu-based Video Stream Publisher

Written by Minsu Jang
Date: 2018-06-09
"""

from __future__ import absolute_import, unicode_literals
import datetime

from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue

import sys
import time

import cv2

# Default RabbitMQ server URI
rabbit_url = 'amqp://guest:guest@localhost:5672//'

# Kombu Connection
conn = Connection(rabbit_url)
channel = conn.channel()

# Kombu Exchange
# - set delivery_mode to transient to prevent disk writes for faster delivery
exchange = Exchange("video-exchange", type="direct", delivery_mode=1)

# Kombu Producer
producer = Producer(exchange=exchange, channel=channel, routing_key="video")

# Kombu Queue
queue = Queue(name="video-queue", exchange=exchange, routing_key="video") 
queue.maybe_bind(conn)
queue.declare()

# Video Capture by OpenCV
capture = cv2.VideoCapture(0)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    ret, frame = capture.read()
    if ret is True:
        # Make image smaller for faster delivery
        frame = cv2.resize(frame, None, fx=0.6, fy=0.6)
        # Encode into JPEG
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        # Send JPEG-encoded byte array
        producer.publish(imgencode.tobytes(), content_type='image/jpeg', content_encoding='binary')
    time.sleep(0.001)

capture.release()

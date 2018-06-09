# Kombu/RabbitMQ-based Video Streaming

This repo includes a simple program that shows how to deliver a video stream using Kombu and RabbitMQ in real-time, with an assumption that the sender and the receiver reside in the same computer system.

[RabbitMQ](https://www.rabbitmq.com) is an open-source message broker.

[Kombu](https://github.com/celery/kombu/) is a python-based messaging library that can use RabbitMQ as a transport.

## Requirements

1. Install RabbitMQ and run the server.
   * Installation guides for difference OS systems including Linux, Windows and Mac OS X are available at [https://www.rabbitmq.com/download.html](https://www.rabbitmq.com/download.html). On Mac OS X, you can install RabbitMQ and run the servcer as a service as follows.
        ```
        brew install rabbitmq
        brew services start rabbitmq
        ```
   * After starting the server, you can access the server monitoring panel at [http://localhost:15672](http://localhost:15672)

1. Install Kombu
   * Installation guide is available at [https://kombu.readthedocs.io/en/latest/introduction.html#installation](https://kombu.readthedocs.io/en/latest/introduction.html#installation). In most systems, it is as simple as:
        ```
        pip install kombu
        ```

1. Install OpenCV and Python Wrapper.
   * Refer to the guide at [https://pypi.org/project/opencv-python/](https://pypi.org/project/opencv-python/). In most systems, it is simply installed by typing:
        ```
        pip install opencv-python
        ```

## Run the program
1. Clone this repository and cd into the repository folder.
    ```
    git clone https://github.com/zebehn/kombu-video-streaming.git
    cd kombu-video-streaming
    ```
2. Run the video stream consumer. As there is no message published yet, it just hangs around.
    ```
    python video_consumer.py
    ```
3. Run the video stream producer. You will see the webcam lights on, a window pops up and shows a video stream captured by your webcam if successful.
    ```
    python video_producer.py
    ```

## Speeding Up Message Delivery
* Set the ```delivery_mode``` of Kombu's ```Exchange``` object to 1, which sets it to a transient mode that does not write message data to disk.
* Shrink image size. With my system, the original webcam image size is 1280x720, and when I resized it to 768x432, I got real-time delivery (29fps publish, 29 delivery, 29 consumer acks, 0 unacked, 0 disk writes)

## Getting Help
If you have any suggestions, bug reports or problems, please report them to the [issue tracker](https://github.com/zebehn/kombu-video-streaming/issues).

## Contributing
You are highly encouraged to improve, refactor or add your idea to this program. Just make pull requests!

## License
This software is licensed under the New BSD-3 License. See the LICENSE file in the top distribution directory for the full license text.
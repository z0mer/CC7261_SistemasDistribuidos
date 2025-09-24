import zmq
from time import time, sleep
import random

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:
    topic = "random".encode("utf-8")
    message = str(random.randint(1, 10)).encode("utf-8")
    print(f"message: {message}", flush=True)
    pub.send_multipart([topic, message])

    topic = "hello".encode("utf-8")
    message = "hello".encode("utf-8")
    print(f"message: {message}", flush=True)
    pub.send_multipart([topic, message])
    sleep(1)

pub.close()
context.close()

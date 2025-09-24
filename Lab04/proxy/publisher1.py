import zmq
from time import time, sleep

context = zmq.Context()
pub = context.socket(zmq.PUB)
pub.connect("tcp://proxy:5555")

while True:
    topic = "tempo".encode("utf-8")
    message = str(time()).encode("utf-8")
    print(f"message: {message}", flush=True)
    pub.send_multipart([topic, message])

    topic = "hello".encode("utf-8")
    message = "hello".encode("utf-8")
    print(f"message: {message}", flush=True)
    pub.send_multipart([topic, message])
    sleep(1)

pub.close()
context.close()

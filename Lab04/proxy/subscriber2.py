import zmq
from time import sleep

context = zmq.Context()
sub = context.socket(zmq.SUB)
#sub.setsockopt_string(zmq.SUBSCRIBE, "")

sub.setsockopt_string(zmq.SUBSCRIBE, "hello")
#sub.setsockopt_string(zmq.SUBSCRIBE, "time")
sub.setsockopt_string(zmq.SUBSCRIBE, "random")

sub.connect("tcp://proxy:5556")

while True:
    message = sub.recv_multipart()
    print(f"message: {message}", flush=True)

sub.close()
context.close()

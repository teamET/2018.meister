import socket
import cv2
import numpy as np
import tensoflow as tf
from icecream import ic
from time import sleep

UDP_IP="localhost"
UDP_PORT=5005

def send(message):
    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
    sleep(0.01)

if __name__ == "__main__":
    send("hello world")
    filename="hello.png"
    while True:
        send("0,0,0,0,0,0,0,0")
        sleep(1)





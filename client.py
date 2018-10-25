import socket
import cv2
from pydarknet import Detector,Image
from icecream import ic

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
#    cap=cv2.VideoCapture(0)
    cfg,weights,data="cfg/yolov3.cfg","yolov3.weights","cfg/coco.data"
    net=Detector(bytes(cfg,encoding="utf-8"),bytes(weights,encoding="utf-8"),0,bytes(data,encoding="utf-8"))
    while True:
        ret,frame=cap.read()
        net.detect(Image(filename))
        send("0,0,0,0,0,0,0,0")





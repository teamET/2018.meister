import socket

UDP_IP="localhost"
UDP_PORT=5005

def send(message):
    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
    sleep(0.01)

send("hello world")



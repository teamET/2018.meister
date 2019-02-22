import socket

target_host="localhost"
target_port=50007

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send(message):
    print(message)
    client.sendto(message.encode(),(target_host,target_port))
    data,addr=client.recvfrom(4096)

send("hello world")

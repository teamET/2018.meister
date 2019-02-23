#-*- encoding: utf-8 -*-
import math
import al5d
import os, sys, inspect,time
from time import sleep
import socket,json
import lynx

H = 80
D = 1000

HOST_ADDR = '127.0.0.1'
HOST_PORT = 50007
DATA_SIZE = 1024

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)


class UDPServer(object):
    """
     x-y-zの座標を受け取るためのUDPサーバ。

    Attributes
    ----------
    addr: str
        ホストのアドレス
    port: str
        ホストのポート
    data_size: int
        socket.recv()のバッファーサイズ
    sock: socket
        UDPソケット
    """
    def __init__(self):
        self.addr = HOST_ADDR
        self.port = HOST_PORT
        self.data_size = DATA_SIZE
        self.sock = None

    def __del__(self):
        if self.sock:
            self.sock.close()

    def run(self):
        """
        Parameters
        ----------
        raw: str
            "関数名/{x:100,y:200,z:400}"
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.addr, self.port))
        while True:
            raw = self.sock.recv(self.data_size).decode()
            try:
                func,data=raw.split("/")
                print(func,data)
                yield func,data
            except:
                print("Error occured",raw)
                continue

def culc_xyz(x,y,z) :
    X = -x
    Y = D-z
    Z = H-y
    print(X,Y,Z)
    return (X,Y,Z)


def main():
    udp = UDPServer()
    for func,data in udp.run():
        print(func,data)
        position = json.loads(data)
        X,Y,Z = culc_xyz(position['x'], position['y'], position['z'])
        lynx.move(X,Y,Z)
#        locals().get(func)(**json.loads(data))
    

if __name__=='__main__':
    main()

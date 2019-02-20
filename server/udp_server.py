import socket
import json
from lynxmoton import move

HOST_ADDR = '127.0.0.1'
HOST_PORT = 50007
DATA_SIZE = 1024


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

def main():
    udp = UDPServer()
    funcs=[
            move
            ]
    for func,data in udp.run():
        locals().get(func)(**json.loads(data))


if __name__ == '__main__':
    main()

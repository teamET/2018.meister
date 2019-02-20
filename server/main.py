import socket
import json

HOST_ADDR = '127.0.0.1'
HOST_PORT = 50007
DATA_SIZE = 1024


def move():
    pass


class UDPServer(object):
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
            "function_name/{x:100,y:200,z:400}"
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.addr, self.port))
        while True:
            raw = self.sock.recv(self.data_size).decode()
            try:
                func, data = raw.split("/")
                print(func, data)
                yield func, data
            except Exception as e:
                print(f"Error occured raw : {raw} , error: {e.message}")
                continue


def main():
    udp = UDPServer()
    funcs = [
        move
    ]
    for func, data in udp.run():
        locals().get(func)(**json.loads(data))


if __name__ == '__main__':
    print("start main")
    main()

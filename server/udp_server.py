import socket

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
        """
         デストラクタでソケットを閉じる。
        """
        if self.sock:
            self.sock.close()

    def run(self):
        """
         UPDサーバを立ち上げ，データが来たらイテレータを返すメソッド。
         送られてくるデータのフォーマットは'x,y,z'を想定。

        Yields
        ------
        recv_data_list: list
            受け取ったデータのリスト['x', 'y', 'z']
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.addr, self.port))
        while True:
            recv_data = self.sock.recv(self.data_size).decode()
            print('received data.'+str(recv_data))
            recv_data_list = str(recv_data).split(',')
            yield recv_data_list


def main():
    """
     クラスUDPServerのテスト。実質無限ループに入っているが，
    イテレータで受け取ったデータをyieldで渡している。
    おそらくこんな感じで，for文の中にサーボの制御も追加する？
    """
    udp = UDPServer()
    for i in udp.run():
        print(i)


if __name__ == '__main__':
    main()

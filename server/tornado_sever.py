from tornado import websocket
from tornado import web
from tornado import ioloop
import cv2
import base64
import json
import redis


class HTTPServerHandler(web.RequestHandler):
    """
    　webpage.htmlを表示するだけのHTTPサーバ。
    """
    def get(self, *args, **kwargs):
        self.render('templates/webpage.html')


class ImageBroadcastingHandler(websocket.WebSocketHandler):
    """
     tornado.websocket.WebsocketHandlerを継承した，画像送信用のWebSocketServer。
     掴むターゲットを指定するためのデータの受け渡しにredisを使用。

    Attributes
    ----------
    redis: RedisHandler
    """
    def open(self, *args, **kwargs):
        """
         WebSocket接続時に呼び出され，redisサーバとの接続，初期化を行う。
        """
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        print('Opened redis server connection.')
        self.redis.delete('available')
        print('Initialized set object \'available\' in redis.')
        self.redis.delete('target')
        print('Initialized string object \'target\' in redis.')
        print('Opened web socket connection.')

    def on_close(self):
        """
         WebSocketがcloseされた時に実行。
        print文のログのみ。
        """
        print('Closed web socket connection.')

    def on_message(self, message):
        """
        　接続されたWebSocketからデータを受け取った時に実行。クライアントには定期的に画像ファイルのリクエストを送るようにさせ，
        'request-img'が送られたら画像データをbase64にして送信し，その他の文字列であった場合は，availableの中にあるものであれば
        redisのtargetに入れる。

        Parameters
        ----------
        message: str
            送られてきた文字列データ
        """
        available = list(map(lambda x: x.decode(), list(self.redis.smembers('available'))))
        if message == 'request-img':
            img = cv2.imread('static/chatapp_demo.png')
            self.send_image(img, available)
        else:
            print('Received data:', message)
            if message in available:
                self.redis.set('target', message)
                print('Inserted data to redis as \'target\'.')
            else:
                print('Not found the data in available.')

    def send_image(self, img, available):
        """
        　WebSocketを使用した画像送信用のメソッド。
        画像イメージをpng形式に圧縮しbase64で送信。

        Parameters
        ----------
        img: numpy.ndarray
            画像データ
        available: list
            現在darknetで検出されている物体のリスト
        """
        r, png_img = cv2.imencode('.png', img)
        if r:
            enc_img = base64.b64encode(png_img).decode('utf-8')
            data = json.dumps({
                'data': enc_img,
                'available': available
            })
            self.write_message(data)


def main():
    app = web.Application([(r'/', HTTPServerHandler), (r'/ws/img', ImageBroadcastingHandler)])
    app.listen(8080)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

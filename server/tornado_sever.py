from tornado import websocket
from tornado import web
from tornado import ioloop
import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import cv2
import numpy as np
import math
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
    zed:
        zedのオブジェクト
    runtime_parameters:
        zedの実行時のパラメータ
    image:
        darknetの検出後のイメージデータ
    depth:
        x, yを決めた上での奥行き
    point_could:
        ポイントクラウド
    """
    def __init__(self, application, request, **kwargs):
        """
        　スーパークラスの初期化__init__()を実行し，また，ZEDの初期化も行う。

        Parameters
        ----------
        application
            super()の引数
        request
            super()の引数
        kwargs
            super()の引数
        """
        super().__init__(application, request, **kwargs)
        self.zed = zcam.PyZEDCamera()
        init_params = zcam.PyInitParameters()
        init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
        init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)
        err = zed.open(init_params)
        if err != tp.PyERROR_CODE.PySUCCESS:
            print("zed open failed")
            exit(1)
        self.runtime_parameters = zcam.PyRuntimeParameters()
        self.runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode
        self.image = core.PyMat()
        self.depth = core.PyMat()
        self.point_cloud = core.PyMat()

    def open(self, *args, **kwargs):
        """
         WebSocket接続時に呼び出される。
        """
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



import socket
import cv2
from pydarknet import Detector,Image
from icecream import ic

import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import math
import numpy as np


# shared object
items={
        "target":None,
        "available":[]
        }

UDP_IP="localhost"
UDP_PORT=50007

def send(message):
    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
    sleep(0.01)

def get_distance(x,y):
    err, point_cloud_value = point_cloud.get_value(x, y)
    distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                         point_cloud_value[1] * point_cloud_value[1] +
                         point_cloud_value[2] * point_cloud_value[2])
    return distance


def main():
    # darknet
    cfg,weights,data="cfg/yolov3.cfg","yolov3.weights","cfg/coco.data"
    net=Detector(bytes(cfg,encoding="utf-8"),bytes(weights,encoding="utf-8"),0,bytes(data,encoding="utf-8"))

    # zed
    zed = zcam.PyZEDCamera()
    init_params = zcam.PyInitParameters()
    init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        print("zed open failed")
        exit(1)
    runtime_parameters = zcam.PyRuntimeParameters()
    runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode

    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()

    while True:
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)
            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            results = net.detect(image)
            print("darknet result",results)
            for cat, score, bounds in results:
                x, y, w, h = bounds
                distance=get_distance(x,y)
                if not np.isnan(distance) and not np.isinf(distance):
                    distance = round(distance)
                    print("Distance to Camera at ({0}, {1}): {2} mm\n".format(x, y, distance))
                    items["available"].appned((
                                cat,
                                score,
                                (x,y,distance,w,h))
                            )
        print(items)
    zed.close()


if __name__ == "__main__":
    main()




import pyzed.camera as zcam
import pyzed.core as mat
import pyzed.defines as sl
import pyzed.types as types
import pyzed.mesh as mesh
import numpy as np

init_params=None

def init():
	init_params=sl.InitParameters()
	init_params.depth_mode=sl.DEPTH_MODE.DEPTH_MODE_ULTRA
	init_params.cooredinate_units=sl.UNIT.UNIT_MILLIMETER

def main():
    image=sl.Mat()
    depth_map=sl.Mat()
    runtime_parameters=sl.RuntimeParameters()
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(image,sl.VIEW.VIEWLEFT)
        zed.retrieve_measure(depth_map,sl.MEASURE.MEASURE_DEPTH)
        print(depth_map)


init()
main()


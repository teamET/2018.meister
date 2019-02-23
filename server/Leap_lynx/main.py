import math
import lynx
import os, sys, inspect,time
from time import sleep

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)

import socket,json
import Leap
class SampleListener(Leap.Listener):
    def on_connect(self,controller):
        print "connected"
    def on_frame(self,controller):
        frame = controller.frame()
        hands = frame.hands
        hand = hands[0] # first hand
        print(hand.palm_position[0],-hand.palm_position[2],hand.palm_position[1])
#        lynx.move(hand.palm_position[0],-hand.palm_position[2],hand.palm_position[1])
        lynx.move(150,150,150)
        lynx.gripper(hand.grab_strength)        
        
def main():
    global led_status
    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    #Controller.set_policy

    while True : pass
    #frame=controller.frame()
    pointable = frame.pointables.frontmost
    direction = pointable.direction
    length = pointable.length
    width = pointable.width
    stabilizedPosition = pointable.stabilized_tip_position
    position = pointable.tip_position
    speed = pointable.tip_velocity
    touchDistance = pointable.touch_distance
    zone = pointable.touch_zone

    
    print "Press Enter to Quit"
    try:
        sys.stdin.readline()
    except KeyboardInterpt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__=='__main__':
    main()

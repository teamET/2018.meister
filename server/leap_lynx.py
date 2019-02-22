import math
import al5d

theta_4 = math.pi/4
y0 = 3.03
L_1 = 5.75
L_2 = 7.375
L_3 = 3.375


a = al5d.AL5D('COM5')
a.init()
a.wrist(theta_4)
a.wrist_rotate(math.pi/2)

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

def inch_to_centimeter(n) :
    return n/2.54

def culc_theta(x,y,z,n) :
    z = z-y0
    X = math.hypot(x,y)		
    theta_1 = math.atan(y/x)
    print(theta_1)
    if theta_1 < 0 : theta_1 = theta_1 + math.pi
    theta_5 = math.atan((L_3*math.sin(theta_4))/(L_2+L_3*math.cos(theta_4)))
    if theta_5 < 0 : theta_5 = theta_5+math.pi
    L_23 = math.hypot((L_3*math.sin(theta_4)),(L_2+L_3*math.cos(theta_4)))
    if (X*X+z*z-L_1*L_1-L_23*L_23)/(2*L_1*L_23) > -1:
        theta_35 = math.acos((X*X+z*z-L_1*L_1-L_23*L_23)/(2*L_1*L_23))
    else :
        theta_35 = math.acos(-1)
    theta_3 = theta_35-theta_5
    theta_6 = math.atan((L_23*math.sin(theta_35))/(L_1+L_23*math.cos(theta_35)))
    if theta_6 < 0 : theta_6 = theta_6 + math.pi
    theta_2 = theta_6+math.atan(z/X)
    if theta_2 > math.pi/2 : theta_2 = theta_2-math.pi

    a.base(theta_1)
    a.shoulder(theta_2)
    a.elbow(theta_3)
    if n == 1.0 : a.gripper(100)
    else : a.gripper(0)
    print(theta_1,theta_2,theta_3,theta_4)


def culc_xyz(x,y,z,n) :
    L = math.sqrt(2*(L_1+L_2)*L_3*math.cos(theta_4)+L_3*L_3+(L_1+L_2)*(L_1+L_2))
    X = L*x/150
    Y = -L*y/150
    Z = L*(z-100)/150
    if (math.sqrt(X*X+Y*Y+Z*Z) < 15)  and (Y > 0) and (Z > y0) :
        culc_theta(X,Y,Z,n)


class SampleListener(Leap.Listener):
    def on_connect(self,controller):
        print "connected"
    def on_frame(self,controller):
        frame = controller.frame()
        hands = frame.hands
        hand = hands[0] # first hand
        culc_xyz(hand.palm_position[0],hand.palm_position[2],hand.palm_position[1],hand.grab_strength)

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

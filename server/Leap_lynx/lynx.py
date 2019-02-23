import math
import al5d

theta_4 = math.pi/4

y0 = 72.3
L_1 = 146.1
L_2 = 183.3
L_3 = 118.1

a = al5d.AL5D('COM5')
a.init()

def move_to_xyz(x,y,z) :
    z = z-y0
    X = math.hypot(x,y)
    D = x*x+y*y+z*z     
    theta_1 = math.atan(x/y)
    if theta_1 < 0 : theta_1 = theta_1+math.pi
    theta_5 = math.atan((L_3*math.sin(theta_4))/(L_2+L_3*math.cos(theta_4)))
    if theta_5 < 0 : theta_5 = theta_5+math.pi
    L_23 = math.hypot((L_3*math.sin(theta_4)),(L_2+L_3*math.cos(theta_4)))
    if (D-L_1*L_1-L_23*L_23)/(2*L_1*L_23) > -1:
        theta_35 = math.acos((D-L_1*L_1-L_23*L_23)/(2*L_1*L_23))
    else :
        theta_35 = math.acos(-1)
    theta_3 = theta_35-theta_5
    theta_6 = math.atan((L_23*math.sin(theta_35))/(L_1+L_23*math.cos(theta_35)))
    theta_2 = theta_6+math.atan(z/X)
    a.move(theta_1,theta_2,theta_3,theta_4)

def gripper(n) :
    if n == 1.0 : percent = 100
    else : percent = 0
    a.gripper(percent)

def move(x,y,z) :
    if x==0 and y==0 and z==0 : a.init()
    elif y>0 and z>0  and 22500<x*x+y*y+(z-y0)*(z-y0)<90000 :
        move_to_xyz(x,y,z)
    else : 
        print("The entered coordinates are invalid.")

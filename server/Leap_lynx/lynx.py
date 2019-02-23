import math
import al5d

theta_4 = math.pi/4
y0 = 3.03
L_1 = 5.75
L_2 = 7.375
L_3 = 4.72441

a = al5d.AL5D('COM5')
a.init()

def centimeter_to_inch(n) :
    return n/2.54

def culc_theta(x,y,z) :
    z = z-y0
    X = math.hypot(x,y)		
    theta_1 = math.atan(y/x)
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
    return (theta_1,theta_2,theta_3,theta_4)

def culc_xyz(x,y,z) :
    L = math.sqrt(2*(L_1+L_2)*L_3*math.cos(theta_4)+L_3*L_3+(L_1+L_2)*(L_1+L_2))
    X = L*x/200
    Y = -L*y/200
    Z = L*(z-50)/300
    if (math.sqrt(X*X+Y*Y+Z*Z) < 16.5)  and (Y > 0) and (Z > y0) :
        move_for_inch(X,Y,Z)
    print(X,Y,Z)

def gripper(n) :
    if n == 1.0 : percent = 100
    else : percent = 0
    a.gripper(percent)

def move_for_inch(x,y,z) :
    theta_1,theta_2,theta_3,theta_4 = culc_theta(x,y,z)  
    a.move(theta_1,theta_2,theta_3,theta_4)

def move_for_centimeter(x,y,z) :
	X = centimeter_to_inch(x)
	Y = centimeter_to_inch(y)
	Z = centimeter_to_inch(z)
	move_for_inch(X,Y,Z)

def move_from_Leap(x,y,z) :
    if x==0 and y==0 and z==0 : a.init()
    culc_xyz(x,y,z)

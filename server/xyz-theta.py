import math

theta_4 = math.pi/4
y0 = 3.03
L_1 = 5.75 
L_2 = 7.375
L_3 = 3.375

def culc(x,y,z) :
	z = z-y0
	X = math.hypot(x,y)
	if y == 0 and x > 0 :
		theta_1 = math.pi/2		
	elif y == 0 and x < 0 :
		theta_1 = -math.pi/2		
	else :
		theta_1 = math.atan(x/y)

	theta_5 = math.atan((L_3*math.sin(theta_4))/(L_2+L_3*math.cos(theta_4)))
	if theta_5 < 0 : theta_5 = theta_5+math.pi
	print("theta_5",theta_5)
	L_23 = math.hypot((L_3*math.sin(theta_4)),(L_2+L_3*math.cos(theta_4)))
	theta_35 = math.acos((X*X+z*z-L_1*L_1-L_23*L_23)/(2*L_1*L_23))
	print("theta_35",theta_35)
	theta_3 = theta_35-theta_5
	print("theta_3",theta_3)
	theta_6 = math.atan((L_23*math.sin(theta_35))/(L_1+L_23*math.cos(theta_35)))
	if theta_6 < 0 : theta_6 = theta_6+math.pi
	print("theta_6",theta_6)
	print(math.atan(z/X))
	theta_2 = theta_6+math.atan(z/X)

	print("theta_2",theta_2)
	return (theta_1,theta_2,theta_3,theta_4)

if __name__ == '__main__':
	print(math.acos(-1))
	x=0
	y=12.92153870665435904760692179929177770551603205349200086906
	z=8.23093652939161284121453715930673947653494825193933184503
	theta_1,theta_2,theta_3,theta_4 = culc(x,y,z)
	print(theta_1,theta_2,theta_3,theta_4)
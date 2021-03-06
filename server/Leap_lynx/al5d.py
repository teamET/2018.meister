import ssc32
import math
import time

BASE = 0
SHOULDER = 1
ELBOW = 2
WRIST = 3
GRIPPER = 4
WRIST_ROTATE = 5
theta_4 = math.pi/4


#Measured from bottom of base to servo center, in meters
SHOULDER_HEIGHT = 0.06985
#Measured from servo centers, in meters
SHOULDER_ELBOW_LENGTH = 0.14605

#Measured from servo centers, in meters
#Longer arm
#ELBOW_WRIST_LENGTH = 0.20955
#Shorter arm)
ELBOW_WRIST_LENGTH = 0.1143

#Measured from wrist servo center to tip of gripper
WRIST_ENDPOINT_LENGTH = 0.100013

#XXX: All interpolation is specific to my arm
class AL5D(object):
    def __init__(self, serial_port='/dev/ttyUSB0'):
        self.ssc32 = ssc32.SSC32(serial_port)

    def init(self):
        """Moves all servos to their initial position"""
        with self.ssc32.move_group():
            self.base(math.pi / 2)
            self.shoulder(-math.pi/2)
            self.elbow(3*math.pi / 4)
            self.wrist(theta_4)
            self.wrist_rotate(math.pi/2)
            self.gripper(50)

    def move(self, theta_1, theta_2, theta_3, theta_4):
    	with self.ssc32.move_group():
	    	self.base(theta_1)
	    	self.shoulder(theta_2)
	    	self.elbow(theta_3)
	    	self.wrist(theta_4)

    def move_done(self):
        return self.ssc32.move_done()

    def wait_for_move(self):
        """Blocks until the current movement is finished"""
        while not self.move_done():
            #Empirical testing suggests that we can't poll more often than 1ms
            time.sleep(0.001)

    def gripper(self, percent, speed=100, time=None):
        """Open/close the gripper
        
        percent (float): the percentage closed that the gripper should be (100% is closed, 0% is open)"""
        assert 0 <= percent <= 100, percent
        self.ssc32.move(GRIPPER, int(1100 + 900*(percent / 100.0)), speed, time)

    def base(self, angle, speed=100, time=None):
        """Rotate the base

        angle: the angle to rotate to [0, pi], positive angles are counter-clockwise. 
        pi/2 is facing directly away from controller board"""
        assert 0 <= angle <= math.pi, angle
        percent = angle / math.pi
        self.ssc32.move(BASE, int(2300 - 1800*percent), speed, time)

    def shoulder(self, angle, speed=100, time=None):
        """Move the shoulder

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is pointing straight up"""
    #    assert -math.pi / 4 <= angle <= math.pi / 4, angle
        percent = angle / (math.pi/2)
        self.ssc32.move(SHOULDER, int(1500 - 400*percent), speed, time)

    def elbow(self, angle, speed=100, time=None):
        """Move the elbow

        angle: the angle to rotate to [0, 7pi/8], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 has the arm fully extended"""
#        assert 0 <= angle <= math.pi * 7.0 / 8.0, angle
        percent = angle / math.pi
        self.ssc32.move(ELBOW, int(660 + 1560*percent), speed, time)

    def wrist(self, angle, speed=100, time=None):
        """Move the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is fully extended"""
#        assert -math.pi / 3 <= angle <= math.pi / 3, angle
        percent = angle / (math.pi / 3)
        self.ssc32.move(WRIST, int(1550 - 800*percent), speed, time)

    def wrist_rotate(self, angle, speed=100, time=None):
        """Rotate the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed looking into the gripper"""
        #The gripper has extra rotational room on the positive side
        assert 0 <= angle <= math.pi, angle
        percent = angle / (math.pi)
        self.ssc32.move(WRIST_ROTATE, int(650 + 1820*percent), speed, time)





from abc import ABCMeta,abstractmethod
from numba import jit
from flask import Flask
import threading

class Motor(metaclass=ABCMeta):
    last=[0 for i in range(4)]
    current_rate=[0 for i in range(4)]
    step=10
    pins=[]
    def __init__(self,pins):
        pass
    def acceleration(self,port,target):
        if target > self.last[port]:
            return  self.last[port]+self.step
        elif target < self.last[port]:
            return self.last[port]-self.step
        else :
            return self.last[port]
    @abstractmethod
    def drive():
        pass

    @abstractmethod
    def drive_pin():
        pass


class PiMotor(Motor):
    self.pi=pigpio.pi()
    def __init__(self):
        print('initialized pin is ',pins)
        self.pins=pins
        for pins in self.pins:
            for pin in pins:
                self.pi.set_mode(pin,pigpio.OUTPUT)

    def drive(self,port,target_rate):
        self.current_rate[port]=target_rate
        print('port',port,'target',target_rate,'current',self.current_rate[port])
        if self.last[port] * target_rate < 0:
            time.sleep(0.0001)
        self.drive_pin(port,self.current_rate[port])
        self.last[port]=self.current_rate[port]
    def drive_pin(self,port,rate,BREAK=False):
        print('port:',port,'pin0,1:',self.pins[port],self.pins[0][0],self.pins[0][1],rate)
        if rate > 0:
            self.pi.set_PWM_dutycycle(self.pins[port][0],rate)
            self.pi.set_PWM_dutycycle(self.pins[port][1],0)
        elif rate <0:
            self.pi.set_PWM_dutycycle(self.pins[port][0],0)
            self.pi.set_PWM_dutycycle(self.pins[port][1],-rate)
        elif BREAK is True:
            self.pi.set_PWM_dutycycle(self.pins[port][0],254)
            self.pi.set_PWM_dutycycle(self.pins[port][1],254)


class TxMotor(Motor):
    def __init__(self):
        pass
    def drive():
        pass
    def drive_pin():
        pass

class Management_screen:
    def __init__(self):
        self.app=Flask(__name__)

    def run():
        self.app.run(debug=True,host='0.0.0.0',post=8080)

    @self.app.route('/')
    def index():
        return "hello world"



def main():
    motor=PiMotor()
    manage=Management_screen()


if __name__ == '__main__':
    main()

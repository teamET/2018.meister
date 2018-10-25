
from abc import ABCMeta,abstractmethod
from icecream import ic
from numba import jit
import server as httpserver
import sys
import socket
import importlib
import threading

MOTOR_NUM=4
pwms=[[0,0] for i in range(MOTOR_NUM)]
mode=0

class  SubUdpServer(threading.Thread):
    def __init__(self,shared_data):
        super(SubUdpServer,self).__init__()
        self.UDP_IP=""
        self.UDP_PORT=5005
        self.backlog=10
        self.bufsize=1024
        self.data=shared_data
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True
    @jit(nogil=True)
    def run(self):
        print('===  Sub Thread Starts===')
        print("PORT",self.UDP_PORT)
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        with closing(sock):
            sock.bind((self.UDP_IP,self.UDP_PORT))
            while True:
                cnt=0
                mes=sock.recv(self.bufsize)
                raw=mes.decode('utf-8')
                print('mes',mes,'raw',raw)
                if raw == 'q':
                    print('Sub process is terminated')
                    break
                elif raw is not '' : #and  self.is_json(raw) ==True:
                    pwm_str=raw.split(',')
                    for pwm in map(int,pwm_str):
                        self.data[cnt]=pwm
                        cnt+=1
                    print(self.data)
                else:
                    print('empty message or not json ')
#                time.sleep(1)

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

    @abstractmethod
    def run():
        pass

class PiMotor(Motor):
    def __init__(self):
        pigpio=importlib.util.find_spec("pigpio")
        if pigpio is None:
            print("pigpio is not found")
            return None
        else:
            print("found pigpio")
        self.pi=pigpio.pi()
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
    @jit(nogil=True)
    def run(self):
        while True:
            ic(pwms)
            for i in range(4):
                self.drive(i,pwms[i]);
class Arm:
    pass


class TxMotor(Motor):
    def __init__(self):
        pass
    def drive():
        pass
    def drive_pin():
        pass

def main():
    motor=PiMotor()
    if motor is None:
        print("pigpio not found")
        exit()

    #udp
    server=SubUdpServer(pwms)
    server.setDaemon(True)
    server.start()

    threads=[
            threading.Thread(target=motor.run),
            threading.Thread(target=httpserver.run)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
#    motor.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterupt:
        print("system interupted")
        sys.exit()

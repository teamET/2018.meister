import threading,os, sys, inspect,time
from time import sleep
import viewer
from viewer import led_status

import socket,json
#  UDP communication

UDP_IP="127.0.1.1"
UDP_IP="192.168.137.132" #raspberry pi ip address
UDP_PORT=5005

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)
#import Leap

#class SampleListener(Leap.Listener):
class SimpleListener():
    def __init__(self):
        global led_status
        self.cnt=0

    def on_connect(self,controller):
        print "connected"

    def mainloop(self):
        if self.cnt>9: self.cnt=0
        """
        set led color here
        range of led_status is 0x0 to 0xff
        """
        led_status[0]=10
        self.send_led(led_status)
        print("main loop",id(led_status))

    def on_frame(self,controller):
        print("on_frame")
        print(controller.frame())
        if self.cnt>9: self.cnt=0
        self.send_led(led_status)

    def send(self,message):
        print("message",message)
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
        
    def send_led(self,pwm):
        print "pwm={}".format(pwm)
        pwm_str=map(str,pwm)
        mes=','.join(pwm_str)
        self.send(mes)

def buildThread():
    v=viewer.viewer()
    v.setDaemon(True)
    v.start()
    
def main():
    buildThread()
    listener=SimpleListener()
    while True:
        listener.mainloop()
        
if __name__  == '__main__':
    main()

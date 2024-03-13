from gpiozero import AngularServo
from time import  sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo1 = AngularServo(19,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo2= AngularServo(21,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo3 = AngularServo(26,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo4= AngularServo(17,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)

def servo_1_rotate(angle):
    while (True):
        for i in range(0,angle,1):
            servo1.angle = i
            sleep(0.01)
        
        for i in range(angle,0,-1):
            servo1.angle = i
            sleep(0.01)

def servo_2_rotate(angle):
    while (True):
        for i in range(0,angle,1):
            servo1.angle = i
            sleep(0.01)
        
        for i in range(angle,0,-1):
            servo1.angle = i
            sleep(0.01)

def servo_3_rotate(angle):
    while (True):
        for i in range(0,angle,1):
            servo1.angle = i
            sleep(0.01)
        
        for i in range(angle,0,-1):
            servo1.angle = i
            sleep(0.01)

def servo_4_rotate(angle):
    while (True):
        for i in range(0,angle,1):
            servo1.angle = i
            sleep(0.01)
        
        for i in range(angle,0,-1):
            servo1.angle = i
            sleep(0.01)

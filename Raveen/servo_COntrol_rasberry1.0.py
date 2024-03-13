from gpiozero import AngularServo
from time import  sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo1 = AngularServo(19,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo2= AngularServo(21,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo3 = AngularServo(26,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo4= AngularServo(17,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)

def servo_1_rotate(angle):
    servo1.angle(angle)
        

def servo_2_rotate(angle):
    servo2.angle(angle)

def servo_3_rotate(angle):
    servo3.angle(angle)
        
def servo_4_rotate(angle):
    servo4.angle(angle)

servo_1_rotate(180)     
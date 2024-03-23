from gpiozero import AngularServo
from time import  sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo1 = AngularServo(19,min_pulse_width = 0.0002,max_pulse_width = 2.5/1000,pin_factory = factory)
servo2= AngularServo(21,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo3 = AngularServo(26,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)
servo4= AngularServo(17,min_pulse_width = 0.0005,max_pulse_width = 2.5/1000,pin_factory = factory)

def servo_1_rotate(angle):
    servo1.angle = angle
        

def servo_2_rotate(angle):
    servo2.angle = angle

def servo_3_rotate(angle):
    servo3.angle = angle
        
def servo_4_rotate(angle):
    servo4.angle = angle-90

servo_2_rotate(32)
servo_3_rotate(-53)

    
def Arm():
    servo_2_rotate(32)
    sleep(2)
    for i in range(-90,25,1):
         servo_1_rotate(i)
         print(i)
         sleep(0.01)
    sleep(1)   
    servo_2_rotate(36)
    sleep(2)
    servo_2_rotate(32)
    sleep(2)
    servo_2_rotate(29)
    sleep(1.8)
    servo_2_rotate(32)     
        
    for i in range(25,-90,-1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01) 
    # servo_3_rotate(0)
    # sleep(2)
# Arm()

def gripper_close():
    servo_2_rotate(32)
    sleep(2)
    for i in range(-42,20,1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01)
         
def gripper_open():
    servo_2_rotate(32)
    sleep(2)
    for i in range(20,-42,-1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01) 

def gripper_up():
    servo_2_rotate(36)
    sleep(0.9)
    servo_2_rotate(32)
    
def gripper_down():
    servo_2_rotate(29)
    sleep(1.8)
    servo_2_rotate(32)
    
    

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
    servo4.angle = angle

servo_2_rotate(-12)
# servo_3_rotate(-53)
# # servo_1_rotate(180)    
# while True:
#     servo_2_rotate(32)
#     sleep(2)
#     for i in range(-90,40,1):
#         servo_1_rotate(i)
#         print(i)
#         sleep(0.01)
            
        
#     for i in range(40,-90,-1):
#         servo_1_rotate(i)
#         print(i)
#         sleep(0.01) 
#     # servo_3_rotate(0)
#     # sleep(2)


#     servo_2_rotate(32)
#     sleep(2)

#     servo_2_rotate(35)
#     sleep(2)

#     servo_2_rotate(32)
#     sleep(2)

#     servo_2_rotate(29)
#     sleep(1.8)
#     servo_2_rotate(32)
#     sleep(2)
    
#     servo_3_rotate(-20)
    
def Arm():
    servo_2_rotate(-12)
    sleep(2)
    for i in range(-90,25,1):
         servo_1_rotate(i)
         print(i)
         sleep(0.01)
    sleep(1)   
    servo_2_rotate(-8)
    sleep(2)
    servo_2_rotate(-12)
    sleep(2)
    servo_2_rotate(-15)
    sleep(1.8)
    servo_2_rotate(-12)     
        
    for i in range(25,-90,-1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01) 
    # servo_3_rotate(0)
    # sleep(2)
# Arm()

def gripper_close():
    servo_2_rotate(-12)
    sleep(1)
    for i in range(-40,60,1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01)
         
def gripper_open():
    servo_2_rotate(-12)
    sleep(1)
    for i in range(60,-40,-1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01) 

def gripper_up():
    servo_2_rotate(-8)
    sleep(2)
    servo_2_rotate(-12)
    
def gripper_down():
    servo_2_rotate(-15)
    sleep(2.1)
    servo_2_rotate(-12)

def gripper_full_close():
    servo_2_rotate(-12)
    sleep(2)
    for i in range(-40,80,1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01)
    
# gripper_open()
# # servo_1_rotate(-20)
# gripper_close()
# gripper_open()
# gripper_up()
# gripper_down()

def shoot():
    servo_2_rotate(-12)
    servo_4_rotate(70)
    sleep(1)
    gripper_down()
    for i in range(60,-10,-1):
         servo_1_rotate(i)
        #  print(i)
         sleep(0.01) 
    servo_4_rotate(-70)



def reload():
    servo_2_rotate(-12)
    sleep(1)
    servo_4_rotate(70)

# gripper_up()
# reload()
# shoot()
# reload()
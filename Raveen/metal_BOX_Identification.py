import RPi.GPIO as GPIO
from time import sleep
from motorRotating import *
from servo_COntrol_rasberry import servo_1_rotate,servo_2_rotate,servo_3_rotate,servo_4_rotate,Arm
from tofsensorreadings import tof1Readings

import metal_BOX_Identification
pin_proxy = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_proxy, GPIO.IN)

def getBox(distance):
    if(distance<30):
        Arm()

def checkMetal():
    return GPIO.input(pin_proxy)


# turnLeft(40)#turn left fromm the middle cicle
# goForward(40)#go forward


# metal = False  #detect metal

# ##detect junction
# #goforward,right,left
# status = 1    #1 - forward,2 - right,3 - left

# while(True):
#     if(status == 1):
#         goForward()
#         status += 1
#     elif(status == 2):
#         turnRight()
#         status += 1
#     else:
#         turnLeft()
#         status += 1

#     while(metal):
#         if(distance_to_box<10):
#             stop()
#             getBox(distance_to_box)
#             metal = checkMetal()
#             if(metal == True):
#                 break
#         else:
#             goForward(40)
#     else:
#         goBackward() #if not a metal go to the junction 
#         #detect T junction
# servo_2_rotate(32)
# sleep(2)
# servo_1_rotate(-90)
# sleep(2)
# servo_1_rotate(32)
# sleep(1)
# servo_1_rotate(25)
# sleep(2)
# for i in range(25,-90,-1):
#     servo_1_rotate(i)
#     # print(i)
#     sleep(0.01)

# sleep(3)
# tof =0
# while True:
#     checkMetal()

#     distance_to_box,tof = tof1Readings()
#     if(distance_to_box<30):
#         # stop()
#         # getBox(distance_to_box)
#         Arm()
#         metal = checkMetal()
#     else:
#         # goForward(40)
#         pass
    
    
# tof.stop_ranging()
# tof.close()





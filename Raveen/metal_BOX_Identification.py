import RPi.GPIO as GPIO
from time import sleep

from motorRotating import goForward,goBackword,turnLeft,turnRight,Stop
from  tofsensorreadings import tof1Readings
from servo_COntrol_rasberry import Arm

pin_proxy = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_proxy, GPIO.IN)

def getBox(distance):
    if(distance<10):
        Arm()

def checkMetal():
    return GPIO.input(pin_proxy)


turnLeft(40)#turn left fromm the middle cicle
goForward(40)#go forward

distance_to_box = tof1Readings()
metal = False  #detect metal

##detect junction
#goforward,right,left
status = 1    #1 - forward,2 - right,3 - left

while(True):
    if(status == 1):
        goForward()
        status += 1
    elif(status == 2):
        turnRight()
        status += 1
    else:
        turnLeft()
        status += 1

    while(metal):
        if(distance_to_box<10):
            Stop()
            getBox(distance_to_box)
            metal = checkMetal()
            if(metal == True):
                break
        else:
            goForward(40)
    else:
        goBackword() #if not a metal go to the junction 
        #detect T junction
    





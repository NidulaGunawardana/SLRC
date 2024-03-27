from Raveen.motorRotating import *
from Raveen.tofsensorreadings import tof1Readings
from Raveen.cuboidToF import *

def wall_follow(sensor,distance_right,distance_left,baseSpeed):
    kp = 0.1
    while True:
        if sensor == "sensor_right":
            instant_distance = tof2Readings()
            error = instant_distance - distance_right
            leftSpeed = baseSpeed + error*kp
            rightSpeed = baseSpeed - error*kp
            
        elif sensor == "sensor_left":
            instant_distance = tof3Readings() # This should be tof3Readings  
            error = instant_distance - distance_left
            leftSpeed = baseSpeed - error*kp
            rightSpeed = baseSpeed + error*kp

        else:
            pass

        leftrightMotor_Forward(leftSpeed,rightSpeed)

        if tof3Readings() < (distance_left - 100):
            return "left"
        elif tof2Readings() < (distance_right - 100):
            return  "right"

def init_measure():
    """Getting the initial measurements(Length and width) of the trash yard"""

    left_right_sensor_dis = 200 # Distance between the left and right tof sensors
    front_dis = tof1Readings() 
    left_dis = tof3Readings()
    right_dis = tof2Readings()

    length = left_dis + right_dis + left_right_sensor_dis
    width = front_dis

    return front_dis, left_dis, right_dis, length, width

front_dis, left_dis, right_dis, length, width = init_measure()
ob_direction = wall_follow("sensor_right",right_dis,left_dis,30)
orientation = None
if ob_direction == "left":
    turnLeft(30) # Turn 90 degrees left
    orientation = 180
elif ob_direction == "right":
    turnRight(30) # Turn 90 degrees right
    orientation = 90
stop()

while tof1Readings() < 100:
    goForward(30)
sttop()


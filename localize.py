from Raveen.motorRotating import *
from Raveen.tofsensorreadings import *
from Raveen.cuboidToF import *
from Raveen.servo_COntrol_rasberry import *
from Neo.align import *
import cv2
import numpy as np


def wall_follow(sensor, distance_right, distance_left, baseSpeed, ob_detect=True):
   
    kp = 0.4
    kd = 0.4
    last_error = 0
    
    while True:
        if sensor == "sensor_right":
            instant_distance = tof2Readings()
            error = instant_distance - distance_right
 
            leftSpeed = baseSpeed + (error * kp + (last_error - error) * kd)
            rightSpeed = baseSpeed - (error * kp + (last_error - error) * kd)

            last_error = error

        elif sensor == "sensor_left":
            instant_distance = tof3Readings()  # This should be tof3Readings
            error = instant_distance - distance_left
            leftSpeed = baseSpeed - error * kp
            rightSpeed = baseSpeed + error * kp

        else:
            pass

        if leftSpeed >= 60:
            leftSpeed = 60 
        if rightSpeed >= 60:
            rightSpeed = 60 
        if rightSpeed < 0:
            rightSpeed = 0
        if leftSpeed < 0:
            leftSpeed = 0

        leftrightMotor_Forward(leftSpeed, rightSpeed)
        if ob_detect == True:
            if tof3Readings() < (distance_left - 100):
                return "left"
            elif tof2Readings() < (distance_right - 100):
                return  "right"

def wall_follow_back(sensor, distance_right, distance_left, baseSpeed, ob_detect=True):
   
    kp = 0.4
    kd = 0.4
    last_error = 0
    
    while True:
        if sensor == "sensor_right":
            instant_distance = tof2Readings()
            error = instant_distance - distance_right
 
            leftSpeed = baseSpeed + (error * kp + (last_error - error) * kd)
            rightSpeed = baseSpeed - (error * kp + (last_error - error) * kd)

            last_error = error

        elif sensor == "sensor_left":
            instant_distance = tof3Readings()  # This should be tof3Readings
            error = instant_distance - distance_left
            leftSpeed = baseSpeed - error * kp
            rightSpeed = baseSpeed + error * kp

        else:
            pass

        if leftSpeed >= 60:
            leftSpeed = 60 
        if rightSpeed >= 60:
            rightSpeed = 60 
        if rightSpeed < 0:
            rightSpeed = 0
        if leftSpeed < 0:
            leftSpeed = 0

        leftrightMotor_Forward(leftSpeed, rightSpeed)
        if ob_detect == True:
            if tof3Readings() < (distance_left - 100):
                return "left"
            elif tof2Readings() < (distance_right - 100):
                return  "right"


def init_measure():
    """Getting the initial measurements(Length and width) of the trash yard"""

    left_right_sensor_dis = 140  # Distance between the left and right tof sensors
    front_dis = tof1Readings()
    left_dis = tof3Readings()
    right_dis = tof2Readings()

    length = left_dis + right_dis + left_right_sensor_dis
    width = front_dis

    return front_dis, left_dis, right_dis, length, width

def find_white(sensor, distance_right, distance_left, baseSpeed):
    
    kp = 0.4
    kd = 0.4
    last_error = 0
    
    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    video_capture.set(4, 480)  # Set the height of the frame
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 120)
    while True:
        ret, image = video_capture.read()
        image = cv2.flip(image, 0)
        image = cv2.flip(image, 1)
        width = int(640)
        height = int(480)

        dimensions = (width, height)
        image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        image = image[120:350, 0:640]
        Blackline = cv2.inRange(image, (140,140,140), (255,255,255))	
        kernel = np.ones((3,3), np.uint8)
        Blackline = cv2.erode(Blackline, kernel, iterations=5)
        Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
        contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        if sensor == "sensor_right":
            instant_distance = tof2Readings()
            error = instant_distance - distance_right
 
            leftSpeed = baseSpeed + (error * kp + (last_error - error) * kd)
            rightSpeed = baseSpeed - (error * kp + (last_error - error) * kd)

            last_error = error

        elif sensor == "sensor_left":
            instant_distance = tof3Readings()  # This should be tof3Readings
            error = instant_distance - distance_left
            leftSpeed = baseSpeed - error * kp
            rightSpeed = baseSpeed + error * kp

        else:
            pass

        if leftSpeed >= 60:
            leftSpeed = 60 
        if rightSpeed >= 60:
            rightSpeed = 60 
        if rightSpeed < 0:
            rightSpeed = 0
        if leftSpeed < 0:
            leftSpeed = 0

        leftrightMotor_Forward(leftSpeed, rightSpeed)
  	
        if len(contours_blk) > 0:	 
            stop()
            return 1
        
        cv2.imshow("Frame",Blackline)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

wall_follow_back("sensor_right", 100, 100, 40)
"""
front_dis, left_dis, right_dis, length, width = init_measure()
width_cons = width
length_cons = length
ob_direction = wall_follow("sensor_right",right_dis,left_dis,40)
orientation = None
if ob_direction == "left":
    front_dis, left_dis, right_dis, length, width = init_measure()
    goForward(40)
    sleep(1.2)
    stop()
    
    turnLeft(40) # Turn 90 degrees left
    sleep(1.95)
    stop()
    
    # while tof1Readings() < (left_dis - 100):
    #     goRight(40)
    #     sleep(0.01)
    orientation = 180
    
    servo_3_rotate(0)
    front_dis, left_dis, right_dis, length, width = init_measure()
    find_white("sensor_right",right_dis, left_dis,40)
    # align_robot()
    sleep(3)
    
    front_dis, left_dis, right_dis, length, width = init_measure()
    while tof1Readings() < width_cons - (left_dis + 140):
        turnRight(40)
        sleep(0.5)
    stop()
    
    
elif ob_direction == "right":
    turnRight(40) # Turn 90 degrees right
    sleep(1.9)
    orientation = 90
stop()

# while tof1Readings() < 100:
#     goForward(30)
#     sleep(0.05)
# stop()
"""


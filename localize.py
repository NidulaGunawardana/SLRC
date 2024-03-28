from Raveen.motorRotating import *
from Raveen.tofsensorreadings import *
from Raveen.cuboidToF import *
from Raveen.servo_COntrol_rasberry import *
from Neo.align import *
import cv2
import numpy as np
from PIL import Image
import math

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

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
        if ob_detect == False:
            if tof1Readings() <= right_cons:
                return "forward"

def wall_follow_back(sensor, distance_right, distance_left, baseSpeed, ob_detect=True):
   
    kp = 0.1
    kd = 0.4
    last_error = 0
    global right_cons
    
    while True:
        if sensor == "sensor_right":
            instant_distance = tof2Readings()
            error = instant_distance - distance_right
 
            leftSpeed = baseSpeed - (error * kp + (last_error - error) * kd)
            rightSpeed = baseSpeed + (error * kp + (last_error - error) * kd)

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

        leftrightMotor_Backward(rightSpeed,leftSpeed)
        if ob_detect == True:
            if tof3Readings() < (distance_left - 100):
                return "left"
            elif tof2Readings() < (distance_right - 100):
                return  "right"
            
        if ob_detect == False:
            if tof1Readings() <= right_cons:
                return "forward"


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

            c = max(contours_blk, key=cv2.contourArea)

            M= cv2.moments(c)

            try:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            except:
                continue
            
            if cy < 100 :   
                break
        
        cv2.imshow("Frame",Blackline)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

front_dis = None
left_dis = None
right_dis = None
length = None
width = None
width_cons = None
length_cons = None
right_cons = None
left_cons = None
ob_direction = None
orientation = None

def yard():
    global front_dis, left_dis, right_dis, length, width, width_cons, length_cons, right_cons, left_cons, ob_direction, orientation
    
    front_dis, left_dis, right_dis, length, width = init_measure()
    width_cons = width
    length_cons = length
    right_cons = right_dis
    left_cons = left_dis
    ob_direction = wall_follow("sensor_right", right_dis, left_dis, 40)
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
        find_white("sensor_right", right_dis, left_dis, 40)
        # align_robot()
        sleep(1)
        print(findHeight())
        
        # front_dis, left_dis, right_dis, length, width = init_measure()
        # while tof1Readings() < width_cons - (left_dis + 140):
        #     turnRight(40)
        #     sleep(0.5)
        turnLeft(40)
        sleep(3.9)
        stop()
        
        front_dis, left_dis, right_dis, length, width = init_measure()
        ob_direction = wall_follow("sensor_left", right_dis, left_dis, 40, False)
        
        if ob_direction == "forward":
            stop()
            turnLeft(40)
            sleep(1.95)
            stop()
            
        front_dis, left_dis, right_dis, length, width = init_measure()
        ob_direction = wall_follow("sensor_right", right_dis, left_dis, 40)
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
            find_white("sensor_right", right_dis, left_dis, 40)
            # align_robot()
            sleep(1)
            print(findHeight())
            
            turnLeft(40)
            sleep(3.9)
            stop()
            
            front_dis, left_dis, right_dis, length, width = init_measure()
            ob_direction = wall_follow("sensor_left", right_dis, left_dis, 40, False)
            
            if ob_direction == "forward":
                stop()
                turnRight(40)
                sleep(1.95)
                stop()
            
            servo_3_rotate(-47)
            front_dis, left_dis, right_dis, length, width = init_measure()
            find_white("sensor_left", right_dis, left_dis, 40)
            stop()
        
    elif ob_direction == "right":
        turnRight(40) # Turn 90 degrees right
        sleep(1.9)
        orientation = 90
    
    stop()
    align_robot()

    # while tof1Readings() < 100:
    #     goForward(30)
    #     sleep(0.05)
    # stop()

def findHeight():
    
    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    video_capture.set(4, 480)  # Set the height of the frame
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 100)
    
    servo_ang = -20
    while True:
        
        servo_3_rotate(servo_ang)
        
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)
        width = int(640)
        height = int(480)

        dimensions = (width, height)
        frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
        
        frame = frame[120:350, 0:640]

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Color thresholding
        ret, thresh = cv2.threshold(
            blur, 155, 255, cv2.THRESH_BINARY
        )  # For the white line

        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(
        thresh.copy(), 1, cv2.CHAIN_APPROX_NONE
        )
        
        
        if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)

                M = cv2.moments(c)

                try:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                except:
                    continue
                
                print(cy)
                
                if cy > 160:
                    
                    dis = tof1Readings() - 15
                    dis = dis - 30
                    print("Distance: ", dis)
                    print(servo_ang)
                
                    # if servo_ang > 0:
                    #     return math.tan(math.radians(servo_ang)) * dis + 130
                    # else:
                    #     return 130 - math.tan(math.radians(-servo_ang)) * dis 
                    if servo_ang < 20 :
                        return "10cm"
                    elif servo_ang < 40:
                        return "15cm"
                    else:
                        return "20cm"
                
                cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
                cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
                servo_ang += 1
                sleep(0.05)
                
                # if servo_ang > 40:
                #     break
    
            
            
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return None   
               
yard()
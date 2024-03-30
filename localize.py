from Raveen.motorRotating import *
from Raveen.tofsensorreadings import *
from Raveen.cuboidToF import *
from Raveen.servo_COntrol_rasberry import *
from Neo.align import *
import cv2
import numpy as np
from PIL import Image
import math
from Nidula.irSensors import *
from Raveen.ledAndPushButtons import *

button = 0
running = True

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
    
    while running:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
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
            elif tof1Readings() <= 150:
                return "end"
        elif ob_detect == False:
            if tof1Readings() <= right_cons:
                return "forward"
        


def wall_follow_back(sensor, distance_right, distance_left, baseSpeed, ob_detect=True):
   
    kp = 0.1
    kd = 0.4
    last_error = 0
    global right_cons
    
    while running:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
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
    global running
    kp = 0.4
    kd = 0.4
    last_error = 0
    
    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    video_capture.set(4, 480)  # Set the height of the frame
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 150)
    while running:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
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

            M = cv2.moments(c)

            try:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            except:
                continue
            print(cy)
            if cy < 160: 
                goForward(40)
                sleep(0.2)   
                stop()
                break
            
            return 0
        
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
    global running
    if push_button() == 0:
        sleep(0.2)
        button_pressed()
    global front_dis, left_dis, right_dis, length, width, width_cons, length_cons, right_cons, left_cons, ob_direction, orientation
    servo_3_rotate(-40)

    height_list = []
    
    front_dis, left_dis, right_dis, length, width = init_measure() # Getting the initial measurements of the yard

    # Defining the initial measurements
    width_cons = width
    length_cons = length
    right_cons = right_dis
    left_cons = left_dis

    ob_direction = wall_follow("sensor_right", right_dis, left_dis, 40) # Giving the direction of the object
    orientation = None
    if ob_direction == "end":
        turnLeft(40)
        sleep(3.9)
        stop()
    elif ob_direction == "left": # If the object is placed left
        # front_dis, left_dis, right_dis, length, width = init_measure() 

        goForward(40) # Moving forward to align with the object
        sleep(1.2)
        stop()
        
        turnLeft(40) # Turn 90 degrees left
        sleep(1.95)
        stop()
        
        # orientation = 180
        
        servo_3_rotate(0) # Setting the camera to find the tower position
        front_dis, left_dis, right_dis, length, width = init_measure() # Getting the measurements to wall follow
        find_white("sensor_right", right_dis, left_dis, 40)
        sleep(1)

        height_list.append(findHeight()) # Finding the height of the object
 
        turnLeft(40) # Turning 180 degrees
        sleep(3.9)
        stop()
        
        front_dis, left_dis, right_dis, length, width = init_measure() # Getting the measurements to wall follow
        ob_direction = wall_follow("sensor_left", right_dis, left_dis, 40, False)
        
        if ob_direction == "forward":
            stop()
            turnLeft(40)
            sleep(1.95)
            stop()
            
        goForward(30)
        sleep(0.5)
        stop()
            
        front_dis, left_dis, right_dis, length, width = init_measure()
        ob_direction = wall_follow("sensor_right", right_dis, left_dis, 40)
        orientation = None

        if ob_direction == "end":
            turnLeft(40)
            sleep(3.9)
            stop()
        elif ob_direction == "left":
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
            height_list.append(findHeight())
            
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
            
            # servo_3_rotate(-47)
            # front_dis, left_dis, right_dis, length, width = init_measure()
            # find_white("sensor_left", right_dis, left_dis, 40)
            # stop()

        
        
    # elif ob_direction == "right":
    #     turnRight(40) # Turn 90 degrees right
    #     sleep(1.9)
    #     orientation = 90
    servo_3_rotate(-47)
    front_dis, left_dis, right_dis, length, width = init_measure()
    find_white("sensor_left", right_dis, left_dis, 40)
    stop()

    stop()
    align_robot()

    max_height = max(height_list)
    if max_height == 10:
        return 10
    elif max_height == 15:
        return 20
    elif max_height == 20:
        return 30


def findHeight():
    global running
    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    video_capture.set(4, 480)  # Set the height of the frame
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 180)
    
    servo_ang = -20
    while running:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
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
                        servo_3_rotate(-40)
                        return 10
                    elif servo_ang < 40:
                        servo_3_rotate(-40)
                        return 15
                    else:
                        servo_3_rotate(-40)
                        return 20
                
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
def button_pressed():
    global button
    global running

    sleep(0.2)
    button = button % 2
    print(button, running)
    if button == 0:
        running = True
    elif button == 1:
        running = False
        stop()
        
def go_yard():
    global running
    base_speed = 37

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 250)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))
    count = 0
    kp = 0.13
    kd = 0.01
    prev_error = 0 
    servo_3_rotate(-47)
    gripper_down()

    while running:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
        if sensor_LEFT() == 0 and sensor_RIGHT() == 0:
            # print("junction detected")
            if count == 0 or count == 1:
                goForward(37)
                sleep(1)      
                count += 1

        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)
        width = int(640)
        height = int(480)

        dimensions = (width, height)
        frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Color thresholding
        ret, thresh = cv2.threshold(
            blur, 150, 255, cv2.THRESH_BINARY
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

            # PID control

            error = 368 - cx
            speed = error * kp + (prev_error - error) * kd
            prev_error = error
            left_speed = base_speed - speed
            right_speed = base_speed + speed

            if left_speed > 100:
                left_speed = 100
            elif left_speed < 0:
                left_speed = 0

            if right_speed > 100:
                right_speed = 100
            elif right_speed < 0:
                right_speed = 0

            leftrightMotor_Forward(left_speed, right_speed)

            # Drawing the lines
            cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            
            cv2.imshow("frame", frame)
            cv2.imshow("threshold", thresh)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        else:
            if sensor_FRONT() == 1:
                stop()
                return "came_to_yard"
    return "stopped"

               
# yard()
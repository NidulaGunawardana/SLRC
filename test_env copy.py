import numpy as np
import cv2

from Raveen.motorRotating import *
from Neo.Colorcircleidentify import *
from Raveen.servo_COntrol_rasberry import *

base_speed = 36 # Setting the base speed of the robot
kp = 0.13 # Setting the Kp value of the robot

# Setting the states of the turns
left_turn = False
right_turn = False
turn_180= False

# Setting the state to 0
cross_count = 0

# Setting the threshold for balck and white
th = 155

# Setting servos
cam_ang = -33 # Setting the camera angle
arm_h = 32 # Setting the gripper height

def junction_matrix(disp,image,size):
    """Draw a matrix of squares on the camera frame and give details of junctions"""

    global th
    x_mat = list()
    y_mat = list()
    ex_mat = list()

    i = 140
    while i <= 620:
        # Top-left and bottom-right coordinates of the rectangle
        start_point = (i - size, 240 - size)
        end_point = (i + size, 240 + size)

        crop_img = image[240 - size:240 + size, i - size: i + size]

        mean_value = cv2.mean(crop_img)[0] 

        if mean_value<th:
            x_mat.append(0)
            cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
        else:
            x_mat.append(1)
            cv2.rectangle(disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED)

        i += 80

    j = 60
    while j <= 420:
        if j != 240:
            # Top-left and bottom-right coordinates of the rectangle
            start_point = (380 - size, j - size)
            end_point = (380 + size, j + size)

            crop_img = image[j - size:  j + size, 380 - size: 380 + size]

            mean_value = cv2.mean(crop_img)[0] 

            if mean_value<th:
                y_mat.append(0)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
            else:
                y_mat.append(1)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED)

        j += 60

    mean_value = cv2.mean(image[10 - size:10 + size,20 - size:20 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (20 - size,10 - size), (20 + size,10 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (20 - size,10 - size), (20 + size,10 + size), (0, 0, 255), thickness=cv2.FILLED)

    mean_value = cv2.mean(image[10 - size:10 + size,620 - size:620 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (620 - size,10 - size), (620 + size,10 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (620 - size,10 - size), (620 + size,10 + size), (0, 0, 255), thickness=cv2.FILLED)

    return x_mat,y_mat,ex_mat


def junction_detection(x_mat,y_mat,ex_mat): 
    """ 1 is referred to white color while 0 is reffered to the black color"""
    if (ex_mat[0] == 1 or ex_mat[1] == 1):
        return "Junction ahead"
    elif (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:6] == [1,1,1,1,1,1] and ex_mat[0:2] == [0,0]):
        return 'cross junction' # cross junction
    elif (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0]):
        return 'T junction' # T junction
    elif (x_mat[0:3] == [1,1,1] and y_mat[1:5] == [1,1,1,1] and ex_mat[0:2] == [0,0]):
        return 'T junction left' # T junction left
    elif (x_mat[0:4] == [1,1,1,1] and x_mat[5:7] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        return 'left right angle' # left right angle
    elif (x_mat[3:7] == [1,1,1,1] and x_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        return 'right right angle' # right right angle
    else:
        return None

def v_feed(video_capture):

    global th

    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    width = int(640)
    height = int(480)

    dimentions = (width,height)
    frame = cv2.resize(frame,dimentions,interpolation=cv2.INTER_AREA)

    # Crop the image
    crop_img = frame[120:400, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Color thresholding
    ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY) # For the white line

    row,column,ex = junction_matrix(frame,thresh,8)
    return row

def junction_now(video_capture):

    global th

    # Capture the frames
    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    width = int(640)
    height = int(480)
    
    dimensions = (width,height)
    frame = cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

    # # Crop the image
    # crop_img = frame[120:400, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)


    # Color thresholding
    ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY) # For the white line

    row,column,ex = junction_matrix(frame,thresh,8)
    
    if row[0] == 1 or row[6] == 1:
        return "Junction Now"
    else:
        return None

def lineFollowing():
    global th
    global left_turn
    global right_turn 
    global turn_180
    global cross_count
    global base_speed

    video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640) # Set the width of the frame
    video_capture.set(4, 480) # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 350)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    while True:

        # Capture the frames
        ret, frame = video_capture.read()
        frame = cv2.flip(frame,0)
        frame = cv2.flip(frame,1)
        width = int(640)
        height = int(480)
        
        dimensions = (width,height)
        frame = cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

        # # Crop the image
        # crop_img = frame[120:400, 0:640]

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
        # Color thresholding
        ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY) # For the white line

        # Find the contours of the frame
        contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
           
        row,column,ex = junction_matrix(frame,thresh,8)
    
        temp = junction_detection(row,column,ex)
        colour_junct = capture_circle_pattern(video_capture)
        print(cross_count)

        if temp != None or colour_junct != None: # print if there is a pre defined junction
            print(temp)
            if temp == "Junction ahead":
                while junction_now(video_capture) == None or capture_circle_pattern(video_capture) == None:
                    goForward(base_speed)
                    sleep(0.05)
                break
                
            if colour_junct != None:

                if colour_junct[2] == "blue":
                    goForward(base_speed)
                    # sleep(0.4)
                    stop()
                    right_turn = True
                    # rightJunct()
                    break
                elif colour_junct[2] == "red":
                    goForward(base_speed)
                    sleep(1)
                    stop()
                    left_turn = True
                    break
                elif colour_junct[2] == "white":
                    goForward(base_speed)
                    # sleep(0.4)
                    stop()
                    right_turn = True
                    # rightJunct()
                    break
                elif colour_junct[2] == "green":
                    goForward(base_speed)
                    # sleep(1)
                    stop()

            else:
                if temp == "left right angle":
                    stop()
                    # global left_turn 
                    left_turn = True
                    # leftJunct()
                    
                    # center_line(video_capture, "left right junction")
                    break

                elif temp == "right right angle":
                    stop()
                    # global right_turn
                    right_turn = True
                    # rightJunct()

                    # center_line(video_capture, "right right junction")
                    break

                elif temp == "T junction left":
                    stop()
                    # global left_turn 
                    left_turn = True
                    # leftJunct()
                    # center_line(video_capture, "T junction left")
                    
                    break

                elif temp == "cross junction":
                    stop()
                    if cross_count == 0:
                        # goForward(30)
                        # sleep(0.1)
                        # stop()

                        left_turn = True
                        # center_line(video_capture, "T junction left")
                        cross_count += 1
                        break
                    elif cross_count == 1:
                        # goForward(30)
                        # sleep(1)
                        # stop()

                        turn_180 = True
                        # center_line(video_capture, "T junction left")
                        cross_count += 1
                        break

                    elif cross_count == 2:
                        # goForward(30)
                        # sleep(0.1)
                        # stop()

                        left_turn = True
                        # center_line(video_capture, "T junction left")
                        cross_count += 1
                        break

                    
        # Find the biggest contour (if detected)
        if len(contours) > 0:

            c = max(contours, key=cv2.contourArea)

            M = cv2.moments(c)

            try:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            except:
                continue

            # PID control
            error = 640/2 - cx + 60
            speed = error*kp
            left_speed = base_speed - speed
            right_speed = base_speed + speed
            
            if left_speed>100:
                left_speed = 100
            elif left_speed <0:
                left_speed = 0
            
            if right_speed>100:
                right_speed = 100
            elif right_speed<0:
                right_speed = 0

            leftrightMotor_Forward(left_speed,right_speed)

            # Drawing the lines
            cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
            cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

        else:
            pass

        # Need to pass the frame to draw, frame to process and the size of the squares in that order
        # Display the resulting frame
        cv2.imshow("frame", frame)
        cv2.imshow("threshold",thresh)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

def rightJunct():
    global right_turn
    global base_speed
    goForward(base_speed)
    sleep(2.3)

    turnRight(40)
    sleep(1)
    right_turn = False
    
def leftJunct():
    global left_turn
    global base_speed
    goForward(base_speed)
    sleep(2)

    turnLeft(40)
    sleep(1)
    left_turn = False

def turn180():
    global turn_180
    turnLeft(40)
    sleep(3.2)
    turn_180 = False
    
# Main loop
while True:

    servo_3_rotate(cam_ang) # Setting the camera angle
    servo_2_rotate(arm_h) # Setting the gripper height
    
    if left_turn:
        leftJunct()
    elif right_turn:
        rightJunct()
    elif turn_180:
        turn180()

    lineFollowing()
    if 0xFF == ord("q"):
        break



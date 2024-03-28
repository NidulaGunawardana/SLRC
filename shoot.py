import numpy as np
import cv2

from Raveen.motorRotating import *
from Raveen.servo_COntrol_rasberry import *
from Raveen.tofsensorreadings import *
from Nidula.irSensors import *
from Neo.align import *

video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
video_capture.set(4, 480)  # Set the height of the frame
video_capture.set(3, 640)  # Set the width of the frame
video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
video_capture.set(cv2.CAP_PROP_EXPOSURE, 180)

def grab_ball():

    base_speed = 30

    # video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # # video_capture = cv2.VideoCapture(0)
    # video_capture.set(3, 640)  # Set the width of the frame
    # video_capture.set(4, 480)  # Set the height of the frame

    # video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    # video_capture.set(cv2.CAP_PROP_EXPOSURE, 250)
    # # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))
    global video_capture

    count = 0
    kp = 0.13
    kd = 0.01
    prev_error = 0 
    ball_grbbed = False
    servo_3_rotate(-47)
    gripper_down()

    while True:
        print(tof1Readings())
        print(count)
        if sensor_LEFT() == 0 and sensor_RIGHT() == 0:
            print("junction detected")
            if count == 0:
                stop()
                turnLeft(40)
                sleep(1.95)
                stop()
                goForward(30)
                sleep(1)
                stop()
                align_robot_a(video_capture)
                sleep(1)
                            
                count += 1
            elif count == 1:
                goForward(37)
                sleep(1)
                stop()
                count += 1
            elif count == 2:
                stop()
                # break
            
        if tof1Readings() < 70 and count == 1 and ball_grbbed == False:
            # print("near wall")
            stop()
            gripper_up()
            gripper_open()
            # while tof1Readings() < 30:
            #     # print("near ball")
            #     goForward(25)
            #     sleep(0.05)
            goForward(25)
            sleep(0.8)
            stop()
            
            gripper_full_close()
            # print("ball grabbed")
            servo_3_rotate(-45)
            goBackward(25)
            sleep(0.9)
            stop()
            turnLeft(40)
            sleep(3.9) 
            align_robot_a(video_capture)
            ball_grbbed = True
            stop()

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

            error = 640 / 2 - cx + 60
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
            pass

def counter_align(box_num):
    global video_capture
    counter_set_height()
    box_abs = abs(box_num)
    # for i in range(0,box_abs):
    #     while counter_exist() == "notexist":
    #         if box_num < 0:
    #             turnLeft(25)
    #         else:
    #             turnRight(25)
    #         sleep(0.05)
    #     sleep(0.1)
    #     stop()
    #     print("box behind")

    #     while counter_exist() == "exist":
    #         if box_num < 0:
    #             turnLeft(25)
    #         else:
    #             turnRight(25)
    #         sleep(0.05)
    #     sleep(0.1)
    #     stop()
    #     print("box aligned")
    #     print(i)
        
    while counter_exist() == "exist":
        if box_num < 0:
            turnLeft(25)
        else:
            turnRight(25)
            sleep(0.05)
    stop()
    print("box behind")

def counter_set_height():
    global video_capture
    
    servo_ang = -45
    while True:
        
        servo_3_rotate(servo_ang)
        
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 0)
        frame = cv2.flip(frame, 1)
        width = int(640)
        height = int(480)

        dimensions = (width, height)
        frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
        
        frame = frame[0:480, 140:500]

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Color thresholding
        ret, thresh = cv2.threshold(
            blur, 80, 255, cv2.THRESH_BINARY
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
                
                if cy > 230:
                    print(servo_ang)
                    break

                cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
                cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
                
                
                
                if servo_ang > 30:
                    break
        servo_ang += 1
        sleep(0.05)
        cv2.imshow("frame", frame)
        cv2.imshow("threshold", thresh)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            return None   

def counter_exist():
    global video_capture
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)
    width = int(640)
    height = int(480)

    dimensions = (width, height)
    frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)
    
    frame = frame[0:480, 180:460]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(
        blur, 80, 255, cv2.THRESH_BINARY
    )  # For the white line

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(
    thresh.copy(), 1, cv2.CHAIN_APPROX_NONE
    )
    cv2.imshow("frame", frame)
    cv2.imshow("threshold", thresh)
    
    if len(contours) > 0:
        return "exist"

    else:
        return "notexist"   
        # c = max(contours, key=cv2.contourArea)

        # M = cv2.moments(c)

        # try:
        #     cx = int(M["m10"] / M["m00"])
        #     cy = int(M["m01"] / M["m00"])
        # except:
        #     continue

        cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
            
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return None  

counter_align(2)
import numpy as np
import cv2

from Raveen.motorRotating import *
from Raveen.servo_COntrol_rasberry import *
from Raveen.tofsensorreadings import *
from Nidula.irSensors import *

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

while True:
    print(count)
    if sensor_LEFT() == 0 and sensor_RIGHT() == 0:
        if count == 0:
            stop()
            turnLeft(40)
            sleep(1.95)
            
            count += 1
        if count == 1:
            goForward(37)
            sleep(1)
            stop()
            count += 1
        if count == 2:
            stop()
            # break
        
    if tof1Readings() < 40 and count == 1:
        print("near wall")
        stop()
        gripper_up()
        gripper_open()
        while tof1Readings() < 30:
            print("near ball")
            goForward(25)
            sleep(0.05)
        stop()
        gripper_full_close()
        print("ball grabbed")
        turnLeft(40)
        sleep(3.9) 
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

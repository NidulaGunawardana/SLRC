import numpy as np
import cv2

from Raveen.motorRotating import *

video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
video_capture.set(3, 160)
video_capture.set(4, 120)
# video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
video_capture.set(cv2.CAP_PROP_EXPOSURE, 400)
print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

kp = 0.07
base_speed = 35

while True:

    # Capture the frames

    ret, frame = video_capture.read()

    # Crop the image

    crop_img = frame[60:120, 0:160]

    # Convert to grayscale

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    

    # Color thresholding

    ret, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Find the contours of the frame

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)
        try:
            cx = int(M["m10"] / M["m00"])
        except:
            cx = 1280/2
        try:
            cy = int(M["m01"] / M["m00"])
        except:
            cy = 720/2

        # PID control
        error = 1280/2 - cx
        speed =  error*kp
        left_speed = base_speed + speed
        right_speed = base_speed - speed
        if left_speed>100:
            left_speed = 100
        elif left_speed <0:
            left_speed = 0
        
        if right_speed>100:
            right_speed = 100
        elif right_speed<0:
            right_speed = 0
        
        
        leftrightMotor_Forward(left_speed,right_speed)
        print(cx, left_speed, right_speed,error)

        # Drawing the lines
        cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

        # if cx >= 120:

        #     print("Turn Left!")

        # if cx < 120 and cx > 50:

        #     print("On Track!")

        # if cx <= 50:

        #     print("Turn Right")

    else:

        print("I don't see the line")

    # Display the resulting frame

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

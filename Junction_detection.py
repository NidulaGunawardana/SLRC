import numpy as np
import cv2

from Raveen.motorRotating import *

base_speed = 35
kp = 0.55

def junction_matrix(disp,image,size):
    x_mat = list()
    y_mat = list()
    ex_mat = list()

    th = 127

    i = 40
    while i <= 280:
        # Top-left and bottom-right coordinates of the rectangle
        start_point = (i - size, 120 - size)
        end_point = (i + size, 120 + size)

        crop_img = image[120 - size:120 + size, i - size: i + size]

        mean_value = cv2.mean(crop_img)[0] 

        if mean_value<th:
            x_mat.append(0)
            cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
        else:
            x_mat.append(1)
            cv2.rectangle(disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED)

        i += 40

    j = 30
    while j <= 210:
        if j != 120:
            # Top-left and bottom-right coordinates of the rectangle
            start_point = (160 - size, j - size)
            end_point = (160 + size, j + size)

            crop_img = image[j - size:  j + size, 160 - size: 160 + size]

            mean_value = cv2.mean(crop_img)[0] 

            if mean_value<th:
                y_mat.append(0)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
            else:
                y_mat.append(1)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED)

        j += 30

    mean_value = cv2.mean(image[60 - size:60 + size,40 - size:40 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (40 - size,60 - size), (40 + size,60 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (40 - size,60 - size), (40 + size,60 + size), (0, 0, 255), thickness=cv2.FILLED)

    mean_value = cv2.mean(image[60 - size:60 + size,280 - size:280 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (280 - size,60 - size), (280 + size,60 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (280 - size,60 - size), (280 + size,60 + size), (0, 0, 255), thickness=cv2.FILLED)

    if (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:6] == [1,1,1,1,1,1] and ex_mat[0:2] == [0,0]):
        return 'cross junction' # cross junction
    elif (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0]):
        return 'T junction' # T junction
    elif (x_mat[0:4] == [1,1,1,1] and x_mat[5:7] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        stop()
        sleep(5)
        return 'left right angle' # left right angle
    elif (x_mat[3:7] == [1,1,1,1] and x_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        stop()
        sleep(5)
        return 'right right angle' # right right angle

  
    else:
        return None
# Main code
video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
video_capture.set(3, 320) # Set the width of the frame
video_capture.set(4, 240) # Set the height of the frame

video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
video_capture.set(cv2.CAP_PROP_EXPOSURE, 200)
print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

while True:

    # Capture the frames

    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    width = int(320)
    height = int(240)
    
    dimentions = (width,height)
    frame = cv2.resize(frame,dimentions,interpolation=cv2.INTER_AREA)


    # Crop the image

    crop_img = frame[60:120, 0:160]

    # Convert to grayscale

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
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
        error = 320/2 - cx
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
        # print(cx, left_speed, right_speed)

        # Drawing the lines
        cv2.line(frame, (cx, 0), (cx, 240), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (320, cy), (255, 0, 0), 1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

    else:

        print("I don't see the line")

    # Need to pass the frame to draw, frame to process and the size of the squares in that order
    print(junction_matrix(frame,thresh,8))

    # Display the resulting frame
    cv2.imshow("frame", frame)
    cv2.imshow("threshold",thresh)
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break




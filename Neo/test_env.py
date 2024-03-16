import numpy as np
import cv2

base_speed = 30
kp = 0.13

def junction_matrix(disp,image,size):
    x_mat = list()
    y_mat = list()
    ex_mat = list()

    th = 127 # Pixel value threshold to detect black and white

    i = 80
    while i <= 560:
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
            start_point = (320 - size, j - size)
            end_point = (320 + size, j + size)

            crop_img = image[j - size:  j + size, 320 - size: 320 + size]

            mean_value = cv2.mean(crop_img)[0] 

            if mean_value<th:
                y_mat.append(0)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
            else:
                y_mat.append(1)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED)

        j += 60

    mean_value = cv2.mean(image[120 - size:120 + size,80 - size:80 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (80 - size,120 - size), (80 + size,120 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (80 - size,120 - size), (80 + size,120 + size), (0, 0, 255), thickness=cv2.FILLED)

    mean_value = cv2.mean(image[120 - size:120 + size,560 - size:560 + size])[0]
    if mean_value<th:
        ex_mat.append(0)
        cv2.rectangle(disp, (560 - size,120 - size), (560 + size,120 + size), (0, 0, 255), 1)
    else:
        ex_mat.append(1)
        cv2.rectangle(disp, (560 - size,120 - size), (560 + size,120 + size), (0, 0, 255), thickness=cv2.FILLED)

    return x_mat,y_mat,ex_mat


def junction_detection(x_mat,y_mat,ex_mat): 
    """ 1 is referred to white color while 0 is reffered to the black color"""

    if (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:6] == [1,1,1,1,1,1] and ex_mat[0:2] == [0,0]):
        return 'cross junction' # cross junction
    elif (x_mat[0:7] == [1,1,1,1,1,1,1] and y_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0]):
        return 'T junction' # T junction
    elif (x_mat[0:4] == [1,1,1,1] and x_mat[5:7] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        return 'left right angle' # left right angle
    elif (x_mat[3:7] == [1,1,1,1] and x_mat[0:2] == [0,0] and ex_mat[0:2] == [0,0] and y_mat[0] == 0):
        return 'right right angle' # right right angle
    else:
        return None

def center_line(x_mat):
    while x_mat[3] == 1:
        # Do what you need to do untill the robo detect the line and alligned with the centre
        pass
    # Stop what you are doing

# Main code
# video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640) # Set the width of the frame
video_capture.set(4, 480) # Set the height of the frame

video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
video_capture.set(cv2.CAP_PROP_EXPOSURE, 200)
print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

while True:

    # Capture the frames

    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    width = int(640)
    height = int(480)
    
    dimentions = (width,height)
    frame = cv2.resize(frame,dimentions,interpolation=cv2.INTER_AREA)


    # Crop the image
    # crop_img = frame[60:120, 0:160]

    # Convert to grayscale

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY) # For the white line
    # ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Find the contours of the frame

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

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
        error = 640/2 - cx
        speed = error*kp
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
        # leftrightMotor_Forward(left_speed,right_speed)
        print(error, left_speed, right_speed)

        # Drawing the lines
        cv2.line(frame, (cx, 0), (cx, 480), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (640, cy), (255, 0, 0), 1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        # print(cx)

    else:

        print("I don't see the line") # pass

    # Need to pass the frame to draw, frame to process and the size of the squares in that order
    row,column,ex = junction_matrix(frame,thresh,10)
    
    temp = junction_detection(row,column,ex)

    if temp != None: # print if there is a pre defined junction
        print(temp)

    # Display the resulting frame
    cv2.imshow("frame", frame)
    cv2.imshow("threshold",thresh)
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break




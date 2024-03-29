import numpy as np
import cv2
from PIL import Image
# from util import get_limits

# video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
# video_capture.set(3, 640) # Set the width of the frame
# video_capture.set(4, 480) # Set the height of the frame

# video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
# video_capture.set(cv2.CAP_PROP_EXPOSURE, 300)
# print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

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


def capture_circle_pattern(video_capture):

    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    width = int(640)
    height = int(480)
    
    dimensions = (width,height)
    frame = cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

    green = [0, 255, 0]  # green in BGR colorspace
    blue = [255, 0, 0]  # blue in BGR colorspace
    red = [0, 0, 255]  # red in BGR colorspace

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit_green, upperLimit_green = get_limits(green)
    lowerLimit_blue, upperLimit_blue = get_limits(blue)
    lowerLimit_red, upperLimit_red = get_limits(red)

    mask_green = cv2.inRange(hsvImage, lowerLimit_green, upperLimit_green)
    mask_blue = cv2.inRange(hsvImage, lowerLimit_blue, upperLimit_blue)
    mask_red = cv2.inRange(hsvImage, lowerLimit_red, upperLimit_red)

    mask_green_ = Image.fromarray(mask_green)
    mask_blue_ = Image.fromarray(mask_blue)
    mask_red_ = Image.fromarray(mask_red)

    bbox_green = mask_green_.getbbox()
    bbox_blue = mask_blue_.getbbox()
    bbox_red = mask_red_.getbbox()
    
    if bbox_green is not None:
        x1, y1, x2, y2 = bbox_green
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
   
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    else:
        return None
 
    if bbox_blue is not None:
        x_1, y_1, x_2, y_2 = bbox_blue
        x_blue = (x_1+x_2)/2
        y_blue = (y_1+y_2)/2
        frame = cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), 3)
    else:
        return None

    if bbox_red is not None:
        x1_, y1_, x2_, y2_ = bbox_red
        x_red = (x1_+x2_)/2
        y_red = (y1_+y2_)/2
        frame = cv2.rectangle(frame, (x1_, y1_), (x2_, y2_), (0, 0, 255), 3)
    else:
        return None
    
    order = list()

    if y_red < y_blue and x_blue<x_red:
        order = ["red","white","blue","green"] #top,down,left,right
    elif y_red < y_blue and x_red<x_blue:
        order = ["green","blue","red","white"] #top,down,left,right
    elif y_blue < y_red and x_red < x_blue:
        order = ["white","red","green","blue"] #top,down,left,right
    elif y_blue<y_red and x_blue < x_red:
        order = ["blue","green","white","red"] #top,down,left,right
    else:
        return None
    
    return order

# while True:
    
#     ret, frame = video_capture.read()
#     frame = cv2.flip(frame,0)
#     frame = cv2.flip(frame,1)
#     width = int(640)
#     height = int(480)

#     dimentions = (width,height)
#     frame = cv2.resize(frame,dimentions,interpolation=cv2.INTER_AREA)

#     print(capture_circle_pattern(frame))
#     cv2.imshow("Frame",frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):

#         break

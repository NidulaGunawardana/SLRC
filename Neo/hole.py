import numpy as np
import cv2
from PIL import Image

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


def capture_hole(video_capture):

    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    width = int(640)
    height = int(480)
    
    dimensions = (width,height)
    frame = cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

    green = [0, 255, 0]  # green in BGR colorspace

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit_green, upperLimit_green = get_limits(green)

    mask_green = cv2.inRange(hsvImage, lowerLimit_green, upperLimit_green)

    mask_green_ = Image.fromarray(mask_green)

    bbox_green = mask_green_.getbbox()

    if bbox_green is not None:
        x1, y1, x2, y2 = bbox_green
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    else:
        return None

    if y2 < 440:
        return "hole"

def capture_wall_color(video_capture):
    
    ret, frame = video_capture.read()
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    width = int(640)
    height = int(480)
    
    dimensions = (width,height)
    frame = cv2.resize(frame,dimensions,interpolation=cv2.INTER_AREA)

    green = [0, 255, 0]  # green in BGR colorspace
    blue = [255,0,0] # green in BGR colorspace

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit_green, upperLimit_green = get_limits(green)
    lowerLimit_blue, upperLimit_blue = get_limits(blue)

    mask_green = cv2.inRange(hsvImage, lowerLimit_green, upperLimit_green)
    mask_blue = cv2.inRange(hsvImage, lowerLimit_blue, upperLimit_blue)

    mask_green_ = Image.fromarray(mask_green)
    mask_green_ = Image.fromarray(mask_blue)

    bbox_green = mask_green_.getbbox()
    bbox_blue = mask_blue.getbbox()

    if bbox_green is not None:
        x1, y1, x2, y2 = bbox_green
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        return "green"
    elif bbox_blue is not None:
        x_1, y_1, x_2, y_2 = bbox_green
        frame = cv2.rectangle(frame, (x_1, y_1), (x_2, y_2), (255, 0, 0), 3)
        return "blue"
    else:
        return None

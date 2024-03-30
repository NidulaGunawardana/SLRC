#!/quanta/bin/env python3

import numpy as np
import cv2

from Raveen.motorRotating import *
from Raveen.servo_COntrol_rasberry import *
from Raveen.tofsensorreadings import tof1Readings, tof4Readings
from Raveen.metal_BOX_Identification import *
from Raveen.ledAndPushButtons import *
from Raveen.cuboidToF import *

from Neo.Colorcircleidentify import *
from Neo.align import *
from Neo.hole import *
from Nidula.irSensors import *
from Nidula.serialCom import *
from localize import *
import box_grab_red_box as box_grab_red
from shoot import shoot_main

base_speed = 37  # Setting the base speed of the robot
kp = 0.13  # Setting the Kp value of the robot  0.13
kd = 0.01  # Setting the Kd value of the robot

# Setting the states of the turns
left_turn = False
left_turn_col = False
right_turn = False
right_turn_col = False
turn_180 = False
turn_180_double = False
go_around_circle = False
mid_object = None

box_grabbed = False
hole_detected = False
finish = False
wall_color = None  # "green"
button = 0
running = False

# Setting the state to 0
cross_count = 0
t_count = 0
box_count = 0
box_existing = False
colour_junction = False
prev_error = 0
distance_samples = []

# Setting the threshold for balck and white
th = 155
exp = 280

# Setting servos
cam_ang = -47  # Setting the camera angle -30 to box normal -47
arm_h = -12  # Setting the gripper height
gem_count = 0


def lineFollowing():
    global th
    global left_turn
    global left_turn_col
    global right_turn
    global right_turn_col
    global turn_180
    global turn_180_double
    global cross_count
    global base_speed
    global box_count
    global box_existing
    global box_grabbed
    global hole_detected
    global wall_color
    global finish
    global cam_ang
    global running
    global colour_junction
    global prev_error
    global kp
    global kd
    global go_around_circle
    global t_count
    global mid_object
    global distance_samples
    global gem_count
    global exp

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, exp)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    while True:
        if push_button() == 0:
            sleep(0.2)
            button_pressed()
        if running:
            # Capture the frames
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
                blur, th, 255, cv2.THRESH_BINARY
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
                # print(cx)

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

            else:
                pass

            # Need to pass the frame to draw, frame to process and the size of the squares in that order
            # Display the resulting frame
            cv2.imshow("frame", frame)
            cv2.imshow("threshold", thresh)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

            colour_junct = capture_circle_pattern(video_capture)

            if colour_junct != None:
                colour_junction = True
                if colour_junct[2] == "blue":
                    goForward(30)
                    sleep(0.6)
                    stop()
                    if wall_color == "blue":
                        left_turn_col = True
                    else:
                        right_turn_col = True
                    break

                elif colour_junct[2] == "red":
                    goForward(30)
                    sleep(0.6)
                    stop()
                    left_turn_col = True
                    break
                elif colour_junct[2] == "white":
                    goForward(30)
                    sleep(0.6)
                    stop()
                    right_turn_col = True
                    break
                elif colour_junct[2] == "green":
                    goForward(30)
                    stop()
            else:

                if cross_count == 2:
                    distance = tof1Readings()
                    print(distance)

                    if box_existing:
                        if distance < 100:
                            if box_count <= 2:
                                box_detection()
                                # turn_180 = True
                                turnLeft(40)
                                sleep(3.9)
                                stop()
                                align_robot_a(video_capture)
                                break
                    else:
                        if box_count == 0:
                            right_turn = True
                            box_count += 1
                            break
                        elif box_count == 1:
                            turn_180_double = True
                            box_count += 1
                            box_existing = True
                            break

                if (
                    capture_hole(video_capture) != None
                    and box_grabbed == True
                    and colour_junct == None
                    and cross_count == 5
                ):
                    # goBackward(30)
                    # sleep(0.3)
                    # stop()
                    # align_robot_a(video_capture)

                    goForward(30)
                    sleep(1.8)
                    stop()
                    gripper_open()
                    goBackward(30)
                    sleep(0.8)
                    stop()

                    gripper_down()
                    # gripper_up_to_push()
                    gripper_full_close()
                    goForward(30)
                    sleep(1.7)
                    goBackward(30)
                    sleep(1.5)
                    stop()

                    turn_180 = True
                    cam_ang = -47
                    break

                row, column, ex = junction_matrix(frame, thresh, 8)

                temp = junction_detection(row, column, ex)
                print(cross_count, box_count)

                if temp != None:  # print if there is a pre defined junction
                    print(temp)
                    if temp == "Junction ahead":
                        while junction_now(video_capture) == None:
                            goForward(30)
                            sleep(0.05)
                        stop()
                        break

                    if temp == "left right angle":
                        stop()
                        left_turn = True
                        break

                    elif temp == "right right angle":
                        stop()
                        right_turn = True
                        break

                    elif temp == "T junction left":
                        stop()
                        left_turn = True
                        servo_3_rotate(20)

                        wall_color = capture_wall_color(video_capture)

                        while wall_color == None:
                            wall_color = capture_wall_color(video_capture)
                        # break

                        if t_count == 1:
                            left_turn = True
                            go_around_circle = False
                            mid_object = cylinder(distance_samples)
                            if mid_object == "cylinder":
                                cylinderLed()
                                gem_count += 10
                            elif mid_object == "box":
                                boxLed()
                                gem_count += 20
                            t_count += 1
                        break

                    elif temp == "circle out":
                        left_turn = True
                        go_around_circle = False
                        print(distance_samples)

                        mid_object = cylinder(distance_samples)
                        if mid_object == "cylinder":
                            cylinderLed()
                        elif mid_object == "box":
                            boxLed()
                        t_count += 1
                        break

                    elif temp == "cross junction":
                        stop()
                        if cross_count == 0:
                            stop()
                            left_turn = True
                            cross_count += 1
                            break
                        elif cross_count == 1:
                            goForward(30)
                            sleep(0.2)
                            stop()
                            box_existance()
                            cross_count += 1

                            break

                        elif cross_count == 2:
                            goForward(30)
                            sleep(0.1)
                            stop()
                            if box_count == 1:
                                left_turn = True
                                # box_existance()

                            elif box_count == 2:
                                goForward(30)
                                sleep(0.5)
                                box_existance()

                            # left_turn = True
                            # center_line(video_capture, "T junction left")
                            # cross_count += 1
                            break

                        elif cross_count == 3:
                            goForward(30)
                            sleep(0.1)
                            stop()
                            if box_count == 0:
                                goForward(30)
                                sleep(0.5)
                            elif box_count == 1:
                                left_turn = True
                            elif box_count == 2:
                                right_turn = True

                            cross_count += 1
                            break

                        elif cross_count == 4:
                            stop()
                            left_turn = True
                            cross_count += 1
                            break

                        elif cross_count == 5:
                            stop()
                            # goForward(30)
                            # sleep(0.5)
                            # stop()
                            left_turn = True
                            cross_count += 1

                            break
                    elif temp == "T junction":
                        stop()
                        # turn_180 = True
                        left_turn = True
                        go_around_circle = True
                        t_count += 1
                        break

            if go_around_circle:
                dis_temp = tof4Readings()
                if dis_temp < 300:
                    distance_samples.append(dis_temp)

            # Find the biggest contour (if detected)

        else:
            break


def center_detect(video_capture):
    """Get the video feed and return the values of the row of the matrix"""

    global th

    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)
    width = int(640)
    height = int(480)

    dimentions = (width, height)
    frame = cv2.resize(frame, dimentions, interpolation=cv2.INTER_AREA)

    # Crop the image
    crop_img = frame[120:400, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)  # For the white line

    row, column, ex = junction_matrix(frame, thresh, 8)
    print(column)
    if column[0] == 1:
        return True
    else:
        return False


def blink():
    "Starting sequence"

    for i in range(2):
        cylinderLed()
        boxLed()
        midLed()
        highLed()
        lowLed()    

    offLed()


def servo_init():
    """Localizing the gripper, adjusting the gripper position"""

    global cam_ang
    servo_3_rotate(cam_ang)
    servo_2_rotate(-12)
    sleep(2)
    servo_2_rotate(-9)
    sleep(3)
    servo_2_rotate(-15)
    sleep(2.2)
    servo_2_rotate(-9)
    sleep(0.5)
    servo_2_rotate(-12)

    for i in range(-40, 80, 1):
        servo_1_rotate(i)
        sleep(0.01)

    servo_1_rotate(90)
    sleep(1)

    for i in range(80, -40, -1):
        servo_1_rotate(i)
        sleep(0.01)
    # blink()


def box_existance():
    """Detecting the existeece of the box and setting the variable accordingly"""

    global box_existing

    distance = tof1Readings()
    if distance < 500:
        box_existing = True
    else:
        box_existing = False


def junction_matrix(disp, image, size):
    """Draw a matrix of squares on the camera frame and give details of junctions"""

    global th
    x_mat = list()
    y_mat = list()
    ex_mat = list()

    i = 128
    while i <= 608:
        # Top-left and bottom-right coordinates of the rectangle
        start_point = (i - size, 240 - size)
        end_point = (i + size, 240 + size)

        crop_img = image[240 - size : 240 + size, i - size : i + size]

        mean_value = cv2.mean(crop_img)[0]

        if mean_value < th:
            x_mat.append(0)
            cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
        else:
            x_mat.append(1)
            cv2.rectangle(
                disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED
            )

        i += 80

    j = 60
    while j <= 420:
        if j != 240:
            # Top-left and bottom-right coordinates of the rectangle
            start_point = (368 - size, j - size)
            end_point = (368 + size, j + size)

            crop_img = image[j - size : j + size, 368 - size : 368 + size]

            mean_value = cv2.mean(crop_img)[0]

            if mean_value < th:
                y_mat.append(0)
                cv2.rectangle(disp, start_point, end_point, (0, 0, 255), 1)
            else:
                y_mat.append(1)
                cv2.rectangle(
                    disp, start_point, end_point, (0, 0, 255), thickness=cv2.FILLED
                )

        j += 60

    mean_value = cv2.mean(image[10 - size : 10 + size, 128 - size : 128 + size])[0]
    if mean_value < th:
        ex_mat.append(0)
        cv2.rectangle(
            disp, (128 - size, 10 - size), (128 + size, 10 + size), (0, 0, 255), 1
        )
    else:
        ex_mat.append(1)
        cv2.rectangle(
            disp,
            (128 - size, 10 - size),
            (128 + size, 10 + size),
            (0, 0, 255),
            thickness=cv2.FILLED,
        )

    mean_value = cv2.mean(image[10 - size : 10 + size, 608 - size : 608 + size])[0]
    if mean_value < th:
        ex_mat.append(0)
        cv2.rectangle(
            disp, (608 - size, 10 - size), (608 + size, 10 + size), (0, 0, 255), 1
        )
    else:
        ex_mat.append(1)
        cv2.rectangle(
            disp,
            (608 - size, 10 - size),
            (608 + size, 10 + size),
            (0, 0, 255),
            thickness=cv2.FILLED,
        )

    return x_mat, y_mat, ex_mat


def junction_detection(x_mat, y_mat, ex_mat):
    """1 is referred to white color while 0 is reffered to the black color"""

    global box_existing
    global wall_color

    if (ex_mat[0] == 1 or ex_mat[1] == 1) and y_mat[5] == 1 and t_count != 1:
        return "Junction ahead"
    elif t_count == 1 and (sensor_LEFT() == 0 or x_mat[0] == 1):
        return "circle out"
    elif (
        x_mat[1:6] == [1, 1, 1, 1, 1]
        and y_mat[1:5] == [1, 1, 1, 1]
        and ex_mat[0:2] == [0, 0]
    ):
        return "cross junction"  # cross junction
    elif (
        x_mat[1:6] == [1, 1, 1, 1, 1] and y_mat[0:2] == [0, 0] and ex_mat[0:2] == [0, 0] and t_count != 1
    ):
        return "T junction"  # T junction
    elif (
        x_mat[0:3] == [1, 1, 1]
        and y_mat[1:5] == [1, 1, 1, 1]
        and ex_mat[0:2] == [0, 0]
        # and wall_color == None
    ):
        return "T junction left"  # T junction left
    elif (
        x_mat[0:4] == [1, 1, 1, 1]
        and x_mat[5:7] == [0, 0]
        and ex_mat[0:2] == [0, 0]
        and y_mat[0] == 0
    ):
        return "left right angle"  # left right angle
    elif (
        x_mat[3:7] == [1, 1, 1, 1]
        and x_mat[0:2] == [0, 0]
        and ex_mat[0:2] == [0, 0]
        and y_mat[0] == 0
    ):
        return "right right angle"  # right right angle
    elif ex_mat[0:2] == [1, 1] and y_mat[0:3] == [1, 1, 1]:
        return "stop"
    else:
        return None


def v_feed(video_capture):
    """Get the video feed and return the values of the row of the matrix"""

    global th

    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)
    width = int(640)
    height = int(480)

    dimentions = (width, height)
    frame = cv2.resize(frame, dimentions, interpolation=cv2.INTER_AREA)

    # Crop the image
    crop_img = frame[120:400, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)  # For the white line

    row, column, ex = junction_matrix(frame, thresh, 8)
    return row


def junction_now(video_capture):
    "Identifying whether we are on the junction"

    global th

    # Capture the frames
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)
    width = int(640)
    height = int(480)

    dimensions = (width, height)
    frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    # # Crop the image
    # crop_img = frame[120:400, 0:640]

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, th, 255, cv2.THRESH_BINARY)  # For the white line

    row, column, ex = junction_matrix(frame, thresh, 8)

    if row[0] == 1 or row[6] == 1:
        return "Junction Now"
    else:
        return None


def box_detection():
    """Grabbing the box if metal or else release the grip"""

    global box_count
    global cross_count
    global box_grabbed
    global cam_ang

    print("Box detected")
    goForward(30)
    sleep(1.5)
    print("Went forward")
    stop()
    gripper_close()
    isMetal = checkMetal()
    if isMetal == 1:
        gripper_up_box()
        cam_ang = -25
        servo_3_rotate(cam_ang)
        box_grabbed = True
        cross_count += 1

    else:
        gripper_open()
        box_count += 1

    servo_2_rotate(-12)
    goForward(30)
    sleep(2)
    stop()


def rightJunct():
    """Turning right when there is no box grabbed"""

    global right_turn
    global base_speed
    global colour_junction
    global exp

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, exp)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    while sensor_LEFT() == 1 and sensor_RIGHT() == 1:
        goForward(33)
        sleep(0.05)
    stop()

    turnRight(33)
    sleep(0.3)

    # while sensor_FRONT() == 1:
    while center_detect(video_capture) == False:
        turnRight(33)
        sleep(0.05)

    stop()
    # # box_existance()
    # if colour_junction:
    #     align_robot()
    #     colour_junction = False
    right_turn = False


def leftJunct():
    """Turning left when a box is not grabbed"""

    global left_turn
    global base_speed
    global colour_junction
    global exp

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, exp)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    while sensor_LEFT() == 1 and sensor_RIGHT() == 1:
        goForward(33)
        sleep(0.05)
    stop()

    turnLeft(33)
    sleep(0.3)

    # while sensor_LEFT() == 1:
    while center_detect(video_capture) == False:
        turnLeft(33)
        sleep(0.05)
    # sleep(0.3)
    stop()

    if t_count == 1:
        goForward(33)
        sleep(0.2)
        stop()
    # if cross_count == 5:
    #     align_robot_a(video_capture)

    left_turn = False


def turn180():
    """Turning 180"""

    global turn_180
    global box_count
    global exp

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, exp)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    # while sensor_FRONT() == 0:
    #     turnLeft(33)
    #     sleep(0.05)
    # turnLeft(33)
    # sleep(0.1)

    turnLeft(33)
    sleep(0.3)

    # while sensor_FRONT() == 1:
    while center_detect(video_capture) == False:
        turnLeft(33)
        sleep(0.05)
    # sleep(0.3)
    stop()
    # sleep(1)

    turn_180 = False


def turn180_double():
    """Turning 180 double"""

    # global turn_180_double
    # global box_count

    # video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # # video_capture = cv2.VideoCapture(0)
    # video_capture.set(3, 640)  # Set the width of the frame
    # video_capture.set(4, 480)  # Set the height of the frame

    # video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    # video_capture.set(cv2.CAP_PROP_EXPOSURE, 270)
    # # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

    # for i in range(2):
    #     # while center_detect(video_capture) == True:
    #     #     turnLeft(33)
    #     #     sleep(0.05)
    #     # # turnLeft(33)
    #     # sleep(0.1)

    #     turnLeft(33)
    #     sleep(0.5)

    #     # while sensor_FRONT() == 1:
    #     while center_detect(video_capture) == False:
    #         turnLeft(33)
    #         sleep(0.05)
    #     # sleep(0.3)
    #     stop()

    # turn_180 = False
    turnLeft(40)
    sleep(3.85)
    stop()
    turn_180_double = False


def rightJunctCol():
    global right_turn_col
    global base_speed
    global colour_junction

    goForward(33)
    sleep(1.6)

    turnRight(40)
    sleep(1.95)
    stop()

    align_robot()
    # if colour_junction:
    #     align_robot()
    #     colour_junction = False
    right_turn_col = False


def leftJunctCol():
    global left_turn_col
    global base_speed
    global colour_junction

    goForward(33)
    sleep(1.6)

    turnLeft(40)
    sleep(1.95)
    stop()

    align_robot()
    # if colour_junction:
    #     align_robot()
    #     colour_junction = False

    left_turn_col = False


def button_pressed():
    """Defining button modes and accessing them"""

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
        global exp
        global th
        global base_speed
        global kp
        global kd
        global left_turn
        global left_turn_col
        global right_turn
        global right_turn_col
        global turn_180
        global turn_180_double
        global go_around_circle
        global mid_object
        global box_grabbed
        global hole_detected
        global finish
        global wall_color
        # global button
        # global running
        global cross_count
        global t_count
        global box_count
        global box_existing
        global colour_junction
        global prev_error
        global distance_samples
        global cam_ang
        global arm_h
        global gem_count

        base_speed = 37  # Setting the base speed of the robot
        kp = 0.13  # Setting the Kp value of the robot  0.13
        kd = 0.01  # Setting the Kd value of the robot

        # Setting the states of the turns
        left_turn = False
        left_turn_col = False
        right_turn = False
        right_turn_col = False
        turn_180 = False
        turn_180_double = False
        go_around_circle = False
        mid_object = None

        box_grabbed = False
        hole_detected = False
        finish = False
        wall_color = None  # "green"
        # button = 0
        # running = False

        # Setting the state to 0
        cross_count = 0
        t_count = 0
        box_count = 0
        box_existing = False
        colour_junction = False
        prev_error = 0
        distance_samples = []

        # Setting the threshold for balck and white
        th = 155
        exp = 280

        # Setting servos
        cam_ang = -47  # Setting the camera angle -30 to box normal -47
        arm_h = -12  # Setting the gripper height
        gem_count = 0
        blink()
        servo_init()
        reload()
        blink()
        offLed()
    button += 1


####################################################################### Main loop ##############################################################################
blink()
servo_init()
reload()
# offLed()
blink()


while finish == False:
    if push_button() == 0:
        sleep(0.2)
        button_pressed()
    if running:
        print(wall_color)
        print(mid_object)

        servo_3_rotate(cam_ang)  # Setting the camera angle
        servo_2_rotate(arm_h)  # Setting the gripper height

        if left_turn:
            leftJunct()
            if box_count == 1:
                box_existance()
            if cross_count == 6:
                yardr = go_yard()
                if yardr == "stopped":
                    button_pressed()
                gripper_open()
                gems = yard()
                if gems == 10:
                    lowLed()
                    gem_count += 10
                elif gems == 20:
                    midLed()
                    gem_count += 20
                else:
                    highLed()
                    gem_count += 30
                state = box_grab_red.metalbox_red()
                if state == "Stopped":
                    button_pressed()
                goForward(30)
                sleep(1)
                stop()
                shoot_main(gem_count)
                break
        elif left_turn_col:
            leftJunctCol()
        elif right_turn:
            rightJunct()
            if box_count == 1:
                box_existance()
        elif right_turn_col:
            rightJunctCol()
        elif turn_180:
            turn180()
            # if box_count == 2 and cross_count == 2:
            #     box_existance()


            # if box_grabbed or cross_count == 3 or cross_count == 2:
            #     goBackward(30)
            #     sleep(2)
            #     stop()
            #     # align_robot()

            # elif :
            #     goBackward(30)
            #     sleep(2.6)
            #     stop()
            #     # align_robot()

            if cross_count == 5:
                goBackward(30)
                sleep(1.3)
                stop()

            align_robot()
        elif turn_180_double:
            turn180_double()
            if box_count == 2 and cross_count == 2:
                box_existance()

        lineFollowing()
        if 0xFF == ord("q"):
            break

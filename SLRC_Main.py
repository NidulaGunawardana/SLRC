#!/quanta/bin/env python3

import numpy as np
import cv2

from Raveen.motorRotating import *
from Raveen.servo_COntrol_rasberry import *
from Raveen.tofsensorreadings import tof1Readings
from Raveen.metal_BOX_Identification import *
from Raveen.ledAndPushButtons import *

from Neo.Colorcircleidentify import *
from Neo.align import *
from Neo.hole import *
from Nidula.irSensors import *

base_speed = 33  # Setting the base speed of the robot
kp = 0.12  # Setting the Kp value of the robot

# Setting the states of the turns
left_turn = False
right_turn = False
left_turn_box = False
right_turn_box = False
turn_180 = False
turn_180_a = False
turn_180_b = False
tt = False

box_grabbed = False
hole_detected = False
finish = False
wall_color = None  # "green"
button = 0
running = False

# Setting the state to 0
cross_count = 0
box_count = 0
box_existing = False
colour_junction = False

# Setting the threshold for balck and white
th = 155

# Setting servos
cam_ang = -47  # Setting the camera angle -30 to box normal -47
arm_h = 32  # Setting the gripper height


def lineFollowing():
    global th
    global left_turn
    global right_turn
    global left_turn_box
    global right_turn_box
    global turn_180
    global turn_180_a
    global turn_180_b
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
    global tt

    video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 640)  # Set the width of the frame
    video_capture.set(4, 480)  # Set the height of the frame

    video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
    video_capture.set(cv2.CAP_PROP_EXPOSURE, 200)
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

            colour_junct = capture_circle_pattern(video_capture)

            if colour_junct != None:
                colour_junction = True
                if colour_junct[2] == "blue":
                    goForward(30)
                    sleep(0.3)
                    stop()
                    if wall_color == "blue":
                        left_turn = True
                    else:
                        right_turn = True
                    break

                elif colour_junct[2] == "red":
                    goForward(30)
                    sleep(0.6)
                    stop()
                    left_turn = True
                    break
                elif colour_junct[2] == "white":
                    goForward(30)
                    sleep(0.6)
                    stop()
                    right_turn = True
                    break
                elif colour_junct[2] == "green":
                    goForward(30)
                    stop()
            else:

                if cross_count == 2:
                    distance, tof = tof1Readings()
                    print(distance)

                    if box_existing:
                        if distance < 100:
                            if box_count <= 2:
                                box_detection()
                                if box_grabbed == True:
                                    turn_180_b = True
                                else:
                                    turn_180_a = True
                                    # box_count += 1
                                break
                    else:
                        if box_count == 0:
                            right_turn = True
                            box_count += 1
                            break
                        elif box_count == 1:
                            turn_180 = True
                            box_count += 1
                            box_existing = True
                            break

                if (
                    capture_hole(video_capture) != None
                    and box_grabbed == True
                    and colour_junct == None
                    and cross_count == 5
                ):
                    goBackward(30)
                    sleep(0.3)
                    stop()
                    align_robot_a(video_capture)

                    goForward(30)
                    sleep(1.8)
                    stop()
                    gripper_open()
                    goBackward(30)
                    sleep(0.8)
                    stop()

                    gripper_down()
                    gripper_up()
                    gripper_full_close()
                    goForward(30)
                    sleep(0.9)
                    goBackward(30)
                    sleep(2.3)
                    stop()

                    turn_180_a = True
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

                    if temp == "left right angle":
                        stop()
                        if box_grabbed == True:
                            left_turn_box = True
                        else:
                            left_turn = True
                        break

                    elif temp == "right right angle":
                        stop()
                        if box_grabbed == True:
                            right_turn_box = True
                        else:
                            right_turn = True
                        break

                    elif temp == "T junction left":
                        stop()
                        left_turn = True
                        servo_3_rotate(20)

                        wall_color = capture_wall_color(video_capture)

                        while wall_color == None:
                            wall_color = capture_wall_color(video_capture)
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
                                left_turn_box = True
                            elif box_count == 2:
                                right_turn_box = True
                            # left_turn_box = True
                            # center_line(video_capture, "T junction left")
                            cross_count += 1
                            break

                        elif cross_count == 4:
                            stop()
                            if box_grabbed == True:
                                left_turn_box = True
                            else:
                                left_turn = True
                            cross_count += 1
                            break

                        elif cross_count == 5:
                            stop()
                            goForward(30)
                            sleep(2.4)
                            stop()
                            left_turn = True
                            break
                    elif temp == "T junction":
                        stop()
                        turn_180_a = True
                        tt = True
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
                error = 640 / 2 - cx + 60
                speed = error * kp
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
        else:
            break


def blink():
    "Starting sequence"

    for i in range(3):
        led_on("green")
        sleep(0.1)
        led_off("green")
        sleep(0.1)
        led_on("blue")
        sleep(0.1)
        led_off("blue")
        sleep(0.1)
    led_on("green")
    sleep(1)
    led_off("green")
    sleep(1)


def servo_init():
    """Localizing the gripper, adjusting the gripper position"""

    global cam_ang
    servo_3_rotate(cam_ang)
    servo_2_rotate(32)
    sleep(2)
    servo_2_rotate(37)
    sleep(2)
    servo_2_rotate(28)
    sleep(2.2)
    servo_2_rotate(35)
    sleep(1.4)
    servo_2_rotate(32)

    for i in range(-40, 20, 1):
        servo_1_rotate(i)
        sleep(0.01)

    servo_1_rotate(25)
    sleep(1)

    for i in range(20, -40, -1):
        servo_1_rotate(i)
        sleep(0.01)


blink()
servo_init()


def box_existance():
    """Detecting the existeece of the box and setting the variable accordingly"""

    global box_existing

    distance, tof = tof1Readings()
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

    i = 140
    while i <= 620:
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
            start_point = (380 - size, j - size)
            end_point = (380 + size, j + size)

            crop_img = image[j - size : j + size, 380 - size : 380 + size]

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

    mean_value = cv2.mean(image[10 - size : 10 + size, 20 - size : 20 + size])[0]
    if mean_value < th:
        ex_mat.append(0)
        cv2.rectangle(
            disp, (20 - size, 10 - size), (20 + size, 10 + size), (0, 0, 255), 1
        )
    else:
        ex_mat.append(1)
        cv2.rectangle(
            disp,
            (20 - size, 10 - size),
            (20 + size, 10 + size),
            (0, 0, 255),
            thickness=cv2.FILLED,
        )

    mean_value = cv2.mean(image[10 - size : 10 + size, 620 - size : 620 + size])[0]
    if mean_value < th:
        ex_mat.append(0)
        cv2.rectangle(
            disp, (620 - size, 10 - size), (620 + size, 10 + size), (0, 0, 255), 1
        )
    else:
        ex_mat.append(1)
        cv2.rectangle(
            disp,
            (620 - size, 10 - size),
            (620 + size, 10 + size),
            (0, 0, 255),
            thickness=cv2.FILLED,
        )

    return x_mat, y_mat, ex_mat


def junction_detection(x_mat, y_mat, ex_mat):
    """1 is referred to white color while 0 is reffered to the black color"""

    global box_existing
    global wall_color

    if (ex_mat[0] == 1 or ex_mat[1] == 1) and y_mat[5] == 1:
        return "Junction ahead"
    elif (
        x_mat[0:7] == [1, 1, 1, 1, 1, 1, 1]
        and y_mat[0:6] == [1, 1, 1, 1, 1, 1]
        and ex_mat[0:2] == [0, 0]
    ):
        return "cross junction"  # cross junction
    elif (
        x_mat[0:7] == [1, 1, 1, 1, 1, 1, 1]
        and y_mat[0:3] == [0, 0, 0]
        and ex_mat[0:2] == [0, 0]
    ):
        return "T junction"  # T junction
    elif (
        x_mat[0:3] == [1, 1, 1]
        and y_mat[1:5] == [1, 1, 1, 1]
        and ex_mat[0:2] == [0, 0]
        and wall_color == None
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
    sleep(1)
    print("Went forward")
    stop()
    gripper_close()
    isMetal = checkMetal()
    if isMetal == 1:
        gripper_up()
        cam_ang = -30
        box_grabbed = True
        cross_count += 1
    else:
        gripper_open()
        box_count += 1
    # tof.stop_ranging()
    # tof.close()
    # servo_2_rotate(34)
    # sleep(1)
    servo_2_rotate(32)
    goBackward(30)
    sleep(1)
    stop()


def rightJunct():
    """Turning right when there is no box grabbed"""

    global right_turn
    global base_speed
    global colour_junction

    goForward(base_speed)
    sleep(1.6)

    turnRight(39)
    sleep(1.85)
    stop()
    # box_existance()
    if colour_junction:
        align_robot()
        colour_junction = False
    right_turn = False


def rightJunctBox():
    """Turning right when a box is grabbed"""

    global right_turn_box
    global base_speed

    goForward(base_speed)
    sleep(1.8)

    turnRight(39)
    sleep(1.8)
    stop()

    # box_existance()
    right_turn_box = False


def leftJunct():
    """Turning left when a box is not grabbed"""

    global left_turn
    global base_speed
    global colour_junction

    goForward(base_speed)
    sleep(1.8)

    turnLeft(39)
    sleep(2.1)
    stop()
    if colour_junction:
        align_robot()
        colour_junction = False
    # box_existance()
    left_turn = False


def leftJunctBox():
    """Turning left when a box is grabbed"""

    global left_turn_box
    global base_speed
    goForward(base_speed)
    sleep(1.6)

    turnLeft(39)
    sleep(1.7)
    stop()
    # box_existance()
    left_turn_box = False


def turn180():
    """Turning 180 v1"""

    global turn_180

    turnLeft(39)
    sleep(3.9)
    stop()
    # box_existance()

    turn_180 = False


def turn180_a():
    """Turning 180 v2"""

    global turn_180_a

    turnLeft(39)
    sleep(3.9)
    stop()
    # box_existance()
    turn_180_a = False


def turn180_b():
    """Turning 180 v3"""

    global turn_180_b

    turnLeft(39)
    sleep(3.9)
    stop()
    # box_existance()
    turn_180_b = False


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
        global left_turn
        global right_turn
        global left_turn_box
        global right_turn_box
        global turn_180
        global turn_180_a
        global turn_180_b

        global box_grabbed
        global hole_detected
        global finish
        global wall_color
        # global button
        # global running
        global cross_count
        global box_count
        global box_existing

        # Setting the threshold for balck and white
        global th

        # Setting servos
        global cam_ang  # Setting the camera angle -30 to box normal -47
        global arm_h  # Setting the gripper height

        left_turn = False
        right_turn = False
        left_turn_box = False
        right_turn_box = False
        turn_180 = False
        turn_180_a = False
        turn_180_b = False

        box_grabbed = False
        hole_detected = False
        finish = False
        wall_color = None
        # button = 0
        # running = False
        cross_count = 0
        box_count = 0
        box_existing = False

        # Setting the threshold for balck and white
        th = 155

        # Setting servos
        cam_ang = -47  # Setting the camera angle -30 to box normal -47
        arm_h = 32  # Setting the gripper height
        blink()
        servo_init()
    button += 1


####################################################################### Main loop ##############################################################################
while True and finish == False:
    if push_button() == 0:
        sleep(0.2)
        button_pressed()
    if running:
        print(wall_color)

        servo_3_rotate(cam_ang)  # Setting the camera angle
        servo_2_rotate(arm_h)  # Setting the gripper height

        if left_turn:
            leftJunct()
            if box_count == 1:
                box_existance()
        elif right_turn:
            rightJunct()
            if box_count == 1:
                box_existance()
        elif right_turn_box:
            rightJunctBox()

        elif left_turn_box:
            leftJunctBox()

        elif turn_180:
            turn180()
            if box_count == 2 and cross_count == 2:
                box_existance()

        elif turn_180_b:
            turn180_b()
            if box_grabbed:
                goBackward(30)
                sleep(2.7)
                stop()
                align_robot()

        elif turn_180_a:
            turn180_a()
            if cross_count == 3 or cross_count == 2:
                goBackward(30)
                sleep(2.6)
                stop()
                align_robot()
            if tt == True:
                align_robot()
                tt == False

            elif cross_count == 5:
                goBackward(30)
                sleep(1)
                stop()
                # cross_count = 4

        lineFollowing()
        if 0xFF == ord("q"):
            break


####################################################################### Main loop
while True and finish == False:
    if push_button() == 0:
        sleep(0.2)
        button_pressed()
    if running:
        print(wall_color)

        servo_3_rotate(cam_ang)  # Setting the camera angle
        servo_2_rotate(arm_h)  # Setting the gripper height

        if left_turn:
            leftJunct()
            if box_count == 1:
                box_existance()
        elif right_turn:
            rightJunct()
            if box_count == 1:
                box_existance()
        elif right_turn_box:
            rightJunctBox()

        elif left_turn_box:
            leftJunctBox()

        elif turn_180:
            turn180()
            if box_count == 2 and cross_count == 2:
                box_existance()

        elif turn_180_b:
            turn180_b()
            if box_grabbed:
                goBackward(30)
                sleep(2.7)
                stop()
                align_robot()

        elif turn_180_a:
            turn180_a()
            if cross_count == 3 or cross_count == 2:
                goBackward(30)
                sleep(2.6)
                stop()
                align_robot()
            if tt == True:
                align_robot()
                tt == False

            elif cross_count == 5:
                goBackward(30)
                sleep(1)
                stop()
                # cross_count = 4

        lineFollowing()
        if 0xFF == ord("q"):
            break


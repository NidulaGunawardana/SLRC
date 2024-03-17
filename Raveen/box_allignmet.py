from motorRotating import *

# let center of the video frame 
video_frame_center_x = 320  
video_frame_center_y = 240  

# let center of the rectangular box
rectangular_box_center_x = 300  
rectangular_box_center_y = 200  

# Calculate the difference in x and y coordinates
delta_x = rectangular_box_center_x - video_frame_center_x
delta_y = rectangular_box_center_y - video_frame_center_y


max_speed = 100

speedS = 10 + delta_x * 0.5
speedX = 10 + delta_y * 0.5

def alignMotor():
    if(delta_x<0):
        goLeft(speedS)
    else:
        goRight(speedS)

    if(delta_y<0):
        goForward(speedX)
    else:
        goBackward(speedX)

alignMotor()

import time
import cv2
import numpy as np
from motorRotating import *

video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
    # video_capture = cv2.VideoCapture(0)
video_capture.set(3, 640)  # Set the width of the frame
video_capture.set(4, 480)  # Set the height of the frame

video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
video_capture.set(cv2.CAP_PROP_EXPOSURE, 250)
    # print(video_capture.get(cv2.CAP_PROP_EXPOSURE))

angle_set = False

while True:
	ret, image = video_capture.read()
	image = cv2.flip(image, 0)
	image = cv2.flip(image, 1)
	Blackline = cv2.inRange(image, (140,140,140), (255,255,255))	
	kernel = np.ones((3,3), np.uint8)
	Blackline = cv2.erode(Blackline, kernel, iterations=5)
	Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
	contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 
	if len(contours_blk) > 0:	 
		blackbox = cv2.minAreaRect(contours_blk[0])
		(x_min, y_min), (w_min, h_min), ang = blackbox
		if ang < -45 :
			ang = 90 + ang
		if w_min < h_min and ang > 0:	  
			ang = (90-ang)*-1
		if w_min > h_min and ang < 0:
			ang = 90 + ang	  
		setpoint = 320
		error = int(x_min - setpoint) 
		ang = int(ang)	 
		box = cv2.boxPoints(blackbox)
		box = np.intp(box)
		cv2.drawContours(image,[box],0,(0,0,255),3)	 
		cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
		cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
		cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)


		# if ang > 0 and ang < 88:
		# 	turnLeft(25)
		# 	sleep(0.01)
		# elif ang<0 and ang > -88:
		# 	turnRight(25)
		# 	sleep(0.01)
		# else:
		# 	stop()
		# 	# break

		if error > 0 and error < 5:
			goLeft(25)
			sleep(0.01)
		elif error < 0 and error > -5:
			goRight(25)
			sleep(0.01)
		else:
			stop()

	cv2.imshow("orginal with line", image)


	key = cv2.waitKey(1) & 0xFF	

	if key == ord("q"):
		break

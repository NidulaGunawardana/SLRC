import time
import cv2
import numpy as np
from Raveen.motorRotating import *
# from motorRotating import *


# video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
#     # video_capture = cv2.VideoCapture(0)
# video_capture.set(3, 640)  # Set the width of the frame
# video_capture.set(4, 480)  # Set the height of the frame

# video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
# video_capture.set(cv2.CAP_PROP_EXPOSURE, 250)
# print(video_capture.get(cv2.CAP_PROP_EXPOSURE))
def align_robot():
	center_set = False
	angle_set = False
	count = 0

	ang_buf = []
	err_buff = []
    # video_capture = cv2.VideoCapture(0)
	video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
	video_capture.set(4, 480)  # Set the height of the frame
	video_capture.set(3, 640)  # Set the width of the frame

	video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
	video_capture.set(cv2.CAP_PROP_EXPOSURE, 200)

	while True:
		ret, image = video_capture.read()
		image = cv2.flip(image, 0)
		image = cv2.flip(image, 1)
		width = int(640)
		height = int(480)

		dimensions = (width, height)
		image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
		image = image[120:350, 0:640]
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
    
			setpoint = 368
			error = int(x_min - setpoint) 
			ang = int(ang)	 
			box = cv2.boxPoints(blackbox)
			box = np.intp(box)
			cv2.drawContours(image,[box],0,(0,0,255),3)	 
			cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
			cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)

			# if (ang > 89 or ang < -89) and (error < 15 or error > 15) and count == 0:
			# 	count += 1
			# 	return

			ang_buf.append(ang)
			err_buff.append(error)
			if len(ang_buf) > 30:
				ang_buf.pop(0)
	
			if len(err_buff) > 30:
				err_buff.pop(0)
	

			if ang > 0 and ang < 89:
				turnLeft(30)
				sleep(0.005)
				angle_set = False
			elif ang<0 and ang > -89:
				turnRight(30)
				sleep(0.005)
				angle_set = False
			else:
				# stop()
				angle_set = True
	

				# break
			# if angle_set:
			if error > 15:
				goRight(35)
				center_set = False
					# sleep(0.01)
					# sleep(0.01)
			elif error < -15:
				goLeft(35)
				center_set = False
					# sleep(0.01)
			else:
				# stop()
				center_set = True
				# break
			# if center_set and angle_set:
			# 	count += 1
			# 	if count > 10:
			# 		if not(ang > 85 or ang <-85):
			# 			angle_set = False
			# 		elif not(error <15 and error > -15):
			# 			center_set = False
			# 		else:		
			# 			stop()
			# 			break
	
			if len(ang_buf) == 30 and len(err_buff) == 30:
				if all(i > 89 for i in ang_buf) or all(i < -89 for i in ang_buf):
					angle_set = False
				if all(i < 15 and i > -15 for i in err_buff):
					center_set = False
				if center_set and angle_set:
					stop()
					break

				


		cv2.imshow("orginal with line", image)


		key = cv2.waitKey(1) & 0xFF	

		if key == ord("q"):
			break

# align_robot()



def align_robot_a(video_capture):
	center_set = False
	angle_set = False
	count = 0

	ang_buf =list()
	err_buff = list()
    # video_capture = cv2.VideoCapture(0)
	# video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
	# video_capture.set(4, 480)  # Set the height of the frame
	# video_capture.set(3, 640)  # Set the width of the frame

	# video_capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # manual mode
	# video_capture.set(cv2.CAP_PROP_EXPOSURE, 250)

	while True:
		ret, image = video_capture.read()
		image = cv2.flip(image, 0)
		image = cv2.flip(image, 1)
		width = int(640)
		height = int(480)

		dimensions = (width, height)
		image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
		image = image[120:390, 0:640]
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
			print(x_min)
			setpoint = 350
			error = int(x_min - setpoint) 
			ang = int(ang)	 
			box = cv2.boxPoints(blackbox)
			box = np.intp(box)
			cv2.drawContours(image,[box],0,(0,0,255),3)	 
			cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
			cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
			cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)

			# if (ang > 89 or ang < -89) and (error < 15 or error > 15) and count == 0:
			# 	count += 1
			# 	return
				
			ang_buf.append(ang)
			err_buff.append(error)
			if len(ang_buf) > 30:
				ang_buf.pop(0)
	
			if len(err_buff) > 30:
				err_buff.pop(0)
	

			if ang > 0 and ang < 89:
				turnLeft(30)
				sleep(0.005)
				angle_set = False
			elif ang<0 and ang > -89:
				turnRight(30)
				sleep(0.005)
				angle_set = False
			else:
				# stop()
				angle_set = True
	

				# break
			# if angle_set:
			if error > 15:
				goRight(35)
				center_set = False
					# sleep(0.01)
					# sleep(0.01)
			elif error < -15:
				goLeft(35)
				center_set = False
					# sleep(0.01)
			else:
				# stop()
				center_set = True
				# break
			# if center_set and angle_set:
			# 	count += 1
			# 	if count > 10:
			# 		if not(ang > 85 or ang <-85):
			# 			angle_set = False
			# 		elif not(error <15 and error > -15):
			# 			center_set = False
			# 		else:		
			# 			stop()
			# 			break
	
			if len(ang_buf) == 30 and len(err_buff) == 30:
				if all(i > 89 for i in ang_buf) or all(i < -89 for i in ang_buf):
					angle_set = False
				if all(i < 15 and i > -15 for i in err_buff):
					center_set = False
				if center_set and angle_set:
					stop()
					break


		# cv2.imshow("orginal with line", image)


		key = cv2.waitKey(1) & 0xFF	

		if key == ord("q"):
			break

# align_robot()
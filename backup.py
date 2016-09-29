#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

Kp = 2
Kd = 1
dt = 0
horLine = 350
colors = [[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0]]
def findCenter(x,color):
	start = time.time()
	count = 0
	sum = 0
	for y in range(0,640):
		#imgc[x][y] = color
		if thresh1[x][y] == 255:
			count += 1
			sum += y
		y += 1
	if count != 0:
		avg = int(sum / count)
	else:
		avg = -1
	x = 0
	for x in range(0,480):
		#imgc[x][avg] = color
		x += 1
	end = time.time()
	print("Get Center : " + str(end - start))
	return avg - 320
def PD(error):
	start = time.time()
	Pvalue = Kp*error
	Dvalue = Kd * (error - dt)
	PD = Pvalue + Dvalue
	end = time.time()
	print("PD : " + str(end - start))
	return PD 
camera = PiCamera()
while 1:
	totalStart = time.time()
	start = time.time()
	print("Init : " + str(time.time() - totalStart))
	rawCapture = PiRGBArray(camera)
	print("RawCap : " + str(time.time() - totalStart))
	time.sleep(0.1)
	camera.capture(rawCapture, format="bgr")
	print("Capture : " + str(time.time() - totalStart))
	imgc = rawCapture.array
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY,use_video_port=True)
	#imgc = cv2.cvtColor(imgc,cv2.COLOR_RGB2BGR)
	startThresh = time.time()
	ret,thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY)
	endThresh = time.time()
	print("Thresh : " + str(endThresh - startThresh))
	#camera.close()
	end = time.time()
	print("Capture Image: " + str(end - start))
	offset = findCenter(horLine,colors[2])
	#print("Offset is: " + str(offset - 320))
	#print("PD returned: " + str(PD(offset)))
	PD(offset)
	dt = offset
	totalEnd = time.time()
	print("Total Time : " + str(totalEnd - totalStart))
	#cv2.imshow("image",imgc)
	#cv2.waitKey(0)
	#cv2.destroyWindow("image")

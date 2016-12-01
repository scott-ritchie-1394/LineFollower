#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2
import io

Kp = 2
Kd = 1
dt = 0
horLine = 200
colors = [[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[255,0,255],[0,255,255],[255,255,255],[0,0,0]]
def convertToBits(number):
	bits = []
	testers = [128,64,32,16,8,4,2,1]
	for x in range(0,8):
		if number & testers[x] == 0:
			bits.append(0)
		else:
			bits.append(1)
	return bits
def testThresh(camera,thresh):
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg',use_video_port=True)
	data = np.fromstring(stream.getvalue(), dtype=np.uint8)
	imgc = cv2.imdecode(data,1)
	img = cv2.cvtColor(imgc,cv2.COLOR_BGR2GRAY)
	thresh1 = cv2.threshold(img,thresh,255,cv2.THRESH_BINARY)
	cv2.imshow("image",thresh1[1])
	cv2.waitKey(0)
with PiCamera() as camera:
	camera.resolution = (320,240)
	myCount = 70
	while myCount < 240:
		print("Current Threshold: " + str(myCount))
		testThresh(camera,myCount)
		myCount += 5 

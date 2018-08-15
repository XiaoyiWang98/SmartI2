import cv2
import numpy as np
import tensorflow as tf
import time
from imutils.video import FPS
import sys
from queue import Queue
from threading import Thread
import datetime
import math

class WebcamVideosStream:
	def __init__(self,src):
		cap = cv2.VideoCapture(src)
		cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J', 'P', 'G')) #4-character code for codec (MJPG)
		cap.set(3, 640) #WIDTH
		cap.set(4, 480) #HEIGT
		self.stream = cap
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False

	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				return
			(self.grabbed,self.frame) = self.stream.read()
	
	def read(self):
		return self.frame

	def stop(self):
		self.stopped = True

class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0
 
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self
 
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
 
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1
 
	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()
 
	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()

if __name__ == '__main__':
	
	# 0 for internal webcam, 1 for usb webcam
	src = 0
	close = 150
	further = 200
	fvs = WebcamVideosStream(src).start()

	face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/3.4.0_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

	var = 1
	while var == 1:

		#make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GYW = 0

		# Capture frame-by-frame
		frame = fvs.read()

		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8),cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		#print(len(faces))
		# Display the resulting frame
		for (x,y,w,h) in faces:
			print(x,y,w,h)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			#assign x,y,w,h to Global Valables
			GXR = x
			GYR = y
			GXW = w
			GXH = h
		print(GXR,GYR,GXW,GYW)
		cv2.imshow('frame',frame)
		#if no face detected
		if GXR != 0:
			#Face position is good
			if GXW >= close and GXH >= close and GXW <= further and GXH <= further:
				X = math.floor(GXR + (GXW/2) - (close/2))
				Y = math.floor(GYR + (GXH/2) - (close/2))
				H = close
				W = close
				cut = frame[Y:(Y+H), X:(X+W)]
				cv2.imshow("cut",cut)
			#Face is too further 
			elif GXW < close or GXH < close:
				print("Please move closer!")
			#Face is too close
			elif GXW > further or GYW > further:
				print("Please more feather1")
		else:
			print("No face detected")

		if cv2.waitKey(1) & 0xFF == ord('q'): # 16.666ms = 1/60hz
			break
	
	cv2.destroyAllWindows()
	fvs.stop()

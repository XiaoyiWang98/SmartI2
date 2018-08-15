import cv2
import numpy as np
import tensorflow as tf
import time
from imutils.video import FPS
import sys
from queue import Queue
from threading import Thread
import datetime


class WebcamVideosStream:
	def __init__(self,src=1):
		cap = cv2.VideoCapture(src)
		cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J', 'P', 'G')) #4-character code for codec (MJPG)
		cap.set(cv2.CAP_PROP_FPS, 30) #frame rate
		cap.set(3, 1980) #WIDTH
		cap.set(4, 1080) #HEIGT
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
	
	fvs = WebcamVideosStream().start()

	face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/3.4.0_1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

	var = 1
	while var == 1:

		GXR = 0
		GYR = 0
		GXW = 0
		GYW = 0

		# Capture frame-by-frame
		frame = fvs.read()

		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8),cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		print(len(faces))
		# Display the resulting frame
		for (x,y,w,h) in faces:
			print(x,y,w,h)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]
			GXR = (x/1920)
			GYR = y/1080
			GXW = w/1920
			GXH = h/1080
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'): # 16.666ms = 1/60hz
			break
	
	cv2.destroyAllWindows()
	fvs.stop()

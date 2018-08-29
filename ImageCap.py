#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-8-16


import cv2
import numpy as np
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

class frameGet:
	def __init__(self):
		GXR = 0
		GYR = 0
		GXW = 0
		GYW = 0

	def Getframe(self, fvs, face_cascade, close, further):
		# make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GYW = 0

		# Capture frame-by-frame
		frame = fvs.read()
		cut = 0
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		# print(len(faces))
		# Display the resulting frame
		for (x, y, w, h) in faces:
			print(x, y, w, h)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			roi_gray = gray[y:y + h, x:x + w]
			roi_color = frame[y:y + h, x:x + w]
			# assign x,y,w,h to Global Valables
			GXR = x
			GYR = y
			GXW = w
			GXH = h
		print(GXR, GYR, GXW, GYW)
		cv2.imshow('frame', frame)
		# if no face detected
		if GXR != 0:
			# Face position is good
			if GXW >= close and GXH >= close and GXW <= further and GXH <= further:
				X = math.floor(GXR + (GXW / 2) - (close / 2))
				Y = math.floor(GYR + (GXH / 2) - (close / 2))
				H = close
				W = close
				cut = frame[Y:(Y + H), X:(X + W)]
				cv2.imshow("cut", cut)
			# Face is too further
			elif GXW < close or GXH < close:
				print("Please move closer!")
			# Face is too close
			elif GXW > further or GYW > further:
				print("Please more further!")
		else:
			print("No face detected, please move further")
		return frame, cut, GXR


class frameRun:
	def __init__(self, device):
		# 0 for internal webcam, 1 for usb webcam
		if device == 0:
			src = 0
			close = 100
			further = 300
		elif device == 1:
			src = 1
			close = 100
			further = 200
		fvs = WebcamVideosStream(src).start()

		#for arrows (instruction)
		middle = cv2.imread("Arrows/mid.jpg")
		up = cv2.imread("Arrows/up.png")
		down = cv2.imread("Arrows/down.jpg")
		left = cv2.imread("Arrows/left.png")
		right = cv2.imread("Arrows/Right.jpg")
		click = cv2.imread("Arrows/click.png")
		cv2.namedWindow("Arrows")


		face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

		var = 1
		i = 0
		Gi = 0
		while var == 1:
			frame, head, GXR = frameGet().Getframe(fvs, face_cascade, close, further)

			if GXR != 0:
				if cv2.waitKey(1) & 0xFF == ord('d'):  # 16.666ms = 1/60hz
					cv2.imwrite("samples/"+str(Gi)+".jpg", head)
					Gi += 1
					i = Gi%6

			if i == 0:
				cv2.imshow("Arrows",middle)
			elif i == 1:
				cv2.imshow("Arrows",up)
			elif i == 2:
				cv2.imshow("Arrows",down)
			elif i == 3:
				cv2.imshow("Arrows",left)
			elif i == 4:
				cv2.imshow("Arrows",right)
			elif i == 5:
				cv2.imshow("Arrows",click)

			if cv2.waitKey(1) & 0xFF == ord('q'):  # 16.666ms = 1/60hz
				break

		cv2.destroyAllWindows()
		fvs.stop()

#Uncommand to direct start image capture process
#if __name__ == '__main__':
	#frameRun(0)

#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-8-16


import cv2
import numpy as np
from threading import Thread
import datetime
import math
import csv

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

	def Getframe(self, fvs, face_cascade, close, further,eye_cascade):
		# make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GXH = 0

		# Capture frame-by-frame
		frame = fvs.read()
		cut = 0
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		# for (x, y, w, h) in faces:
		# 	cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
		# 	roi_gray = gray[y:y + h, x:x + w]
		# 	roi_color = img[y:y + h, x:x + w]
		# 	eyes = eye_cascade.detectMultiScale(roi_gray)
		# 	for (ex, ey, ew, eh) in eyes:
		# 		cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
		# print(len(faces))
		# Display the resulting frame
		ex = 0
		ey = 0
		eh = 0
		ew = 0
		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			roi_gray = gray[y:y + h, x:x + w]
			roi_color = frame[y:y + h, x:x + w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
			#assign x,y,w,h to Global Valables
				GXR = ex+x
				GYR = ey+y
				GXW = ew
				GXH = eh
		print(GXR, GYR, GXW, GXH)
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
				cv2.rectangle(roi_color, (X, Y), (X+W, Y+H), (0, 255, 0), 2)
			# Face is too further
			elif GXW < close or GXH < close:
				print("Please move closer!")
			# Face is too close
			elif GXW > further or GXW > further:
				print("Please more further!")
		else:
			print("No face detected, please move further")
		return frame, cut, GXR


class frameRun:
	def __init__(self, device):
		# 0 for internal webcam, 1 for usb webcam
		if device == 0:
			src = 0
			close = 30
			further = 40
		elif device == 1:
			src = 1
			close = 30
			further = 40
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
		eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
		var = 1

		i = 0
		middlei = 1
		upi = 1
		downi = 1
		lefti = 1
		righti = 1
		clicki = 1
		Gi = 0

		#0,1,1,1,1,1,1,0
		with open('index.csv', "r") as f:
			print("Index Loaded")
			f_csv = csv.reader(f)
			row = next(f_csv)
			#print(headers)
			#for row in f_csv:
			print(row)
			i = int(row[0])
			middlei = int(row[1])
			upi = int(row[2])
			downi = int(row[3])
			lefti = int(row[4])
			righti = int(row[5])
			clicki = int(row[6])
			Gi = int(row[7])


		while var == 1:
			frame, head, GXR = frameGet().Getframe(fvs, face_cascade, close, further, eye_cascade)

			if GXR != 0:
				if cv2.waitKey(1) & 0xFF == ord('d'):  # 16.666ms = 1/60hz
					if Gi <= 1000:
						if i == 0:
							cv2.imwrite("samples/train/middle/middle"+str(middlei)+".jpg", head)
							middlei += 1
						elif i == 1:
							cv2.imwrite("samples/train/up/up"+str(upi)+".jpg", head)
							upi += 1
						elif i == 2:
							cv2.imwrite("samples/train/down/down"+str(downi)+".jpg", head)
							downi += 1
						elif i == 3:
							cv2.imwrite("samples/train/left/left"+str(lefti)+".jpg", head)
							lefti += 1
						elif i == 4:
							cv2.imwrite("samples/train/right/right"+str(righti)+".jpg", head)
							righti += 1
						elif i == 5:
							cv2.imwrite("samples/train/click/click"+str(clicki)+".jpg", head)
							clicki += 1
					elif Gi > 1000 & Gi <= 1300:
						if i == 0:
							cv2.imwrite("samples/Validation/middle/middle"+str(middlei)+".jpg", head)
							middlei += 1
						elif i == 1:
							cv2.imwrite("samples/Validation/up/up"+str(upi)+".jpg", head)
							upi += 1
						elif i == 2:
							cv2.imwrite("samples/Validation/down/down"+str(downi)+".jpg", head)
							downi += 1
						elif i == 3:
							cv2.imwrite("samples/Validation/left/left"+str(lefti)+".jpg", head)
							lefti += 1
						elif i == 4:
							cv2.imwrite("samples/Validation/right/right"+str(righti)+".jpg", head)
							righti += 1
						elif i == 5:
							cv2.imwrite("samples/Validation/click/click"+str(clicki)+".jpg", head)
							clicki += 1
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
				rows = [(i, middlei, upi, downi, lefti, righti, clicki, Gi)]
				print(rows)
				with open('index.csv',"w") as f:
					f_csv = csv.writer(f)
					f_csv.writerows(rows)
				break


		cv2.destroyAllWindows()
		fvs.stop()

#Uncommand to direct start image capture process
if __name__ == '__main__':
	frameRun(0)

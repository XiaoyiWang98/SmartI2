#Prediction program for eye
#Xiaoyi(Sean) Wang
#2019-01-08


import cv2
import numpy as np
from threading import Thread
import datetime
import math
from classificationOutput2 import classify
import pyautogui
from validate_model import className
import csv
from IndexMachine import GenerateDataSet

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

class frameGet:

	def Getframe(self, fvs, face_cascade, close, further,eye_cascade):
		# make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GXH = 0

		# Capture frame-by-frame
		frame = fvs.read()
		frame = hisEqulColor(frame)
		cut = 0
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		ref_x = 0
		FXR = 0
		for (x, y, w, h) in faces:
			#cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
			roi_gray = gray[y:y + h, x:x + w]
			roi_color = frame[y:y + h, x:x + w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			FXR = x
			for (ex, ey, ew, eh) in eyes:

				rx = int((ex+0.5*ew)-0.5*close)
				ry = int((ey+0.5*eh)-0.5*close)
				rw = rh = close
				#cv2.rectangle(roi_color, (rx, ry), (rx + rw, ry + rh), (0, 255, 0), 2)
			#assign x,y,w,h to Global Valables
				ref_x = ex
				GXR = ex+x
				GYR = ey+y
				GXW = ew
				GXH = eh
				cv2.rectangle(roi_color, (GXR, GYR), (GXR + GXW, GYR + GXH), (0, 255, 0), 2)
				break

		cv2.imshow('frame', frame)
		# if no face detected
		Y = 0;
		H = 0;
		if FXR != 0 and GXR != ref_x:
			# Face position is good
			if GXW >= close and GXH >= close and GXW <= further and GXH <= further:
				X = math.floor(GXR + (GXW / 2) - (close / 2))
				Y = math.floor(GYR + (GXH / 2) - (close / 2))
				H = close
				W = close
				cut = frame[Y:(Y + H), X:(X + W)]
				cv2.imshow("cut", cut)
				cv2.rectangle(roi_color, (X, Y), (X+W, Y+H), (0, 255, 0), 2)

		return frame, cut, GXR, Y, H


class framePredict:
	def __init__(self, device):

		actions = 4

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

		#Read index

		cv2.namedWindow("head")

		miu_list, theta = classify.classifyInit(0,4)
		print(miu_list)


		while var == 1:
			frame, head, GXR, Y, H = frameGet().Getframe(fvs, face_cascade, close, further, eye_cascade)

			if GXR != 0 and Y != 0 and H != 0:
				head = cv2.cvtColor(head.astype(np.uint8), cv2.COLOR_BGR2GRAY)
				actions = classify.classifySingleImage2(0, head, miu_list, theta, 4)
				self.ImgSandP2(head)

			# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> middle; 5 -> click
			if actions == 0:
				cv2.imshow("Arrows",up)
				pyautogui.moveRel(0, -10, duration=0.025)
			elif actions == 1:
				cv2.imshow("Arrows",down)
				pyautogui.moveRel(0, 10, duration=0.025)
			elif actions == 2:
				cv2.imshow("Arrows",left)
				pyautogui.moveRel(-10, 0, duration=0.025)
			elif actions == 3:
				cv2.imshow("Arrows",right)
				pyautogui.moveRel(10, 0, duration=0.025)
			elif actions == 4:
				cv2.imshow("Arrows",middle)
			elif actions == 5:
				cv2.imshow("Arrows",click)

			if cv2.waitKey(1) & 0xFF == ord('q'):  # 16.666ms = 1/60hz
				break


		cv2.destroyAllWindows()
		fvs.stop()


	def ImgSandP2(self,head):
		cv2.imshow('head', head)

def hisEqulColor(img):
	ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
	channels = cv2.split(ycrcb)
	cv2.equalizeHist(channels[0], channels[0])
	cv2.merge(channels, ycrcb)
	cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
	return img


#Uncommand to direct start image capture process
if __name__ == '__main__':
	framePredict(0)
#Prediction program for eye
#Xiaoyi(Sean) Wang
#2019-01-08


import cv2
import numpy as np
from threading import Thread
import math
from classificationOutput2 import classify
import pyautogui

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

	def Getframe(self, fvs, close, further, eye_cascade,mouth_cascade, closeM, furtherM):
		# make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GXH = 0
		MXR = 0
		MYR = 0
		MXW = 0
		MXH = 0



		# Capture frame-by-frame
		frame = fvs.read()
		frame = hisEqulColor(frame)
		eyecut = None
		Mouthcut = None


		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		eyes = eye_cascade.detectMultiScale(gray)
		mouth = mouth_cascade.detectMultiScale(gray, 1.7, 11)


		for (ex, ey, ew, eh) in eyes:
			GXR = ex
			GYR = ey
			GXW = ew
			GXH = eh
			break

		for (mx, my, mw, mh) in mouth:
			MXR = mx
			MYR = my
			MXW = mw
			MXH = mh
			break

		cv2.imshow('frame', frame)
		# if no eye detected
		Y = 0;
		H = 0;
		Flag = 0
		if GXR != 0 and MXR != 0:
			# Face position is good
			#if GXW >= close and GXH >= close and GXW <= further and GXH <= further:
			X = math.floor(GXR + (GXW / 2) - (close / 2))
			Y = math.floor(GYR + (GXH / 2) - (close / 2))
			H = close
			W = close
			eyecut = frame[Y:(Y + H), X:(X + W)]
			cv2.imshow("Eycut", eyecut)

			MX = math.floor(MXR + (MXW / 2) - (closeM / 2))
			MY = math.floor(MYR + (MXH / 2) - (3 * closeM / 5))
			MH = closeM
			MW = closeM
			Mouthcut = frame[MY:(MY + MH), MX:(MX + MW)]

			cv2.imshow("Mouthcut", Mouthcut)
			Flag = 1

		return frame, eyecut, Mouthcut, Flag


class framePredict:
	def __init__(self, device):

		actionsE = 4
		actionsM = 6

		# 0 for internal webcam, 1 for usb webcam
		if device == 0:
			src = 0
			close = 30
			further = 40
			closeM = 50
			furtherM = 50
		elif device == 1:
			src = 1
			close = 30
			further = 40
			closeM = 50
			furtherM = 50
		fvs = WebcamVideosStream(src).start()

		#for arrows (instruction)
		middle = cv2.imread("Arrows/mid.jpg")
		up = cv2.imread("Arrows/up.png")
		down = cv2.imread("Arrows/down.jpg")
		left = cv2.imread("Arrows/left.png")
		right = cv2.imread("Arrows/Right.jpg")
		click = cv2.imread("Arrows/click.png")
		FNoOp = cv2.imread("Arrows/FNoOp.png")
		cv2.namedWindow("Arrows")

		eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
		Mouth_cascade = cv2.CascadeClassifier('MouthDetector/cascades/haarcascade_mcs_mouth.xml')

		var = 1

		#Read index

		cv2.namedWindow("EyeFrame")
		cv2.namedWindow("MouthFrame")

		miu_listE, thetaE = classify.classifyInit(0,4)
		miu_listM, thetaM = classify.classifyInit(0,2)


		while var == 1:
			frame, eye, mouth, Flag = frameGet().Getframe(fvs, close, further, eye_cascade, Mouth_cascade, closeM, furtherM)
			if Flag == 1:
				eye = cv2.cvtColor(eye.astype(np.uint8), cv2.COLOR_BGR2GRAY)
				mouth = cv2.cvtColor(mouth.astype(np.uint8), cv2.COLOR_BGR2GRAY)
				#actionsE = classify.classifySingleImage2(0, eye, miu_listE, thetaE, 4)
				actionsM = classify.classifySingleImage2(0, mouth, miu_listM, thetaM, 2)
				self.ImgSandP2(eye,mouth)

			# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> noPredictionResult; 5 -> click (mouth_open); 6 -> force_eye_noOp

			if actionsM == 5:
				cv2.imshow("Arrows", click)
			elif actionsM == 6:
				cv2.imshow("Arrows", FNoOp)
			else:
				cv2.imshow("Arrows", middle)
			# if actionsE == 0:
			# 	cv2.imshow("Arrows",up)
			# 	pyautogui.moveRel(0, -10, duration=0.025)
			# elif actionsE == 1:
			# 	cv2.imshow("Arrows",down)
			# 	pyautogui.moveRel(0, 10, duration=0.025)
			# elif actionsE == 2:
			# 	cv2.imshow("Arrows",left)
			# 	pyautogui.moveRel(-10, 0, duration=0.025)
			# elif actionsE == 3:
			# 	cv2.imshow("Arrows",right)
			# 	pyautogui.moveRel(10, 0, duration=0.025)
			# else:
			# 	cv2.imshow("Arrows",middle)


			if cv2.waitKey(1) & 0xFF == ord('q'):  # 16.666ms = 1/60hz
				break


		cv2.destroyAllWindows()
		fvs.stop()


	def ImgSandP2(self,eye,mouth):
		cv2.imshow('EyeFrame', eye)
		cv2.imshow("MouthFrame",mouth)

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
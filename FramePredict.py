#Prediction program for eye
#Xiaoyi(Sean) Wang
#2019-01-08


import cv2
import numpy as np
from threading import Thread
import math
from classificationOutput2 import classify
import os
import shutil
import pyautogui
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

class frameGet:

	def Getframe(self, fvs, close, face_cascade, eye_cascade,mouth_cascade, closeM, furtherM):
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
		eyecut = None
		Mouthcut = None

		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		eyes = eye_cascade.detectMultiScale(gray)
		mouth = mouth_cascade.detectMultiScale(gray, 1.7, 11)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		FX = 0
		FY = 0
		FW = 0
		FH = 0

		for (x, y, w, h) in faces:
			FX = x
			FY = y
			FW = w
			FH = h


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
		# if no eye detected
		Y = 0;
		H = 0;
		FlagM = 0
		FlagE = 0
		if GXR != 0 and MXR != 0 and GYR != 0 and MYR != 0:
			# Face position is good
			#if GXW >= close and GXH >= close and GXW <= further and GXH <= further:
			X = math.floor(GXR + (GXW / 2) - (close / 2))
			Y = math.floor(GYR + (GXH / 2) - (close / 2))
			H = close
			W = close
			if X > 0 and Y > 0:
				eyecut = frame[Y:(Y + H), X:(X + W)]
				FlagE = 1

			MX = math.floor(MXR + (MXW / 2) - (closeM / 2))
			MY = math.floor(MYR + (MXH / 2) - ((3 * closeM )/ 5))
			MH = closeM
			MW = closeM
			print(MX,MY,MH,MW)
			if MX > 0 and MY > 0:
				Mouthcut = frame[MY:(MY + MH), MX:(MX + MW)]
				FlagM = 1

		return frame, eyecut, Mouthcut, FlagE, FlagM, FX, FY, FW, FH


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

		# if os.path.isdir("CurrentData/1000"):
		# 	shutil.rmtree('CurrentData/1000')
		#
		# if os.path.isdir("MouthDetector/CurrentData/1000"):
		# 	shutil.rmtree('MouthDetector/CurrentData/1000')

		flag = 0

		eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
		Mouth_cascade = cv2.CascadeClassifier('MouthDetector/cascades/haarcascade_mcs_mouth.xml')
		face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

		with open('CurrentData/1000/FacePos.csv') as f2:
			f_csv2 = csv.reader(f2)
			for row2 in f_csv2:
				FXAVG, FYAVG, FWAVG, FHAVG = int(row2[0]), int(row2[1]), int(row2[2]), int(row2[3])


		var = 1

		#Read index

		miu_listE, thetaE = classify.classifyInit(0,4)
		miu_listM, thetaM = classify.classifyInit(0,3)

		while var == 1:
			frame, eye, mouth, FlagE, FlagM, FX, FY, FW, FH = frameGet().Getframe(fvs, close, face_cascade, eye_cascade, Mouth_cascade, closeM, furtherM)

			disp = frame
			cv2.rectangle(disp, (FXAVG, FYAVG), (FXAVG + FWAVG, FYAVG + FHAVG), (0, 255, 0), 3)
			cv2.rectangle(disp, (FX, FY), (FX + FW, FY + FH), (255, 0, 0), 3)


			cv2.imshow("Arrow", disp)
			cv2.moveWindow('Arrow', 500, 200)

			if FlagE == 1 and FlagM:
				eye = cv2.cvtColor(eye.astype(np.uint8), cv2.COLOR_BGR2GRAY)
				actionsM = classify.classifySingleImage2(0, mouth, miu_listM, thetaM, 3)
				actionsE = classify.classifySingleImage2(0, eye, miu_listE, thetaE, 4)
<<<<<<< HEAD
				self.ImgSandP2(eye,mouth)

			# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> noPredictionResult; 5 -> click (mouth_open); 6 -> force_eye_noOp

			# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> click (mouth_open); 5 -> forceNoOp; 6 -> mouth_nothing
=======
>>>>>>> 3237dac6478a183fdf25567290903da4c3ee5891

			if actionsM == 4:
				print(str(actionsM)+" Mouth Open    Click")
				if flag == 0:
					flag = 1
			elif actionsM == 5:
				print(str(actionsM) + " Pursing lips    ForceNoOp")
				if flag == 1:
					flag = 0
			elif actionsM == 6:
				print(str(actionsM) + " Mouth Normal    Nothing")

				if flag == 1:
					pyautogui.click()
					flag = 0

				if flag == 1:
					pyautogui.click()
					flag = 0
				if actionsE == 0:
					pyautogui.moveRel(0, -15, duration=0.025)
				elif actionsE == 1:
					pyautogui.moveRel(0, 15, duration=0.025)
				elif actionsE == 2:
					pyautogui.moveRel(-15, 0, duration=0.025)
				elif actionsE == 3:
					pyautogui.moveRel(15, 0, duration=0.025)

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


def hisEqulColor(img):
	ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
	channels = cv2.split(ycrcb)
	cv2.equalizeHist(channels[0], channels[0])
	cv2.merge(channels, ycrcb)
	cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
	return img

def getImageIntensity(img):
	grayscaleImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	width = img.shape[0]
	height = img.shape[1]

	sumIntensity = 0
	for i in range(width):
		for j in range(height):
			sumIntensity = sumIntensity + grayscaleImage[i,j]
	
	return (sumIntensity/grayscaleImage.size)
			




#Uncommand to direct start image capture process
if __name__ == '__main__':
	framePredict(0)
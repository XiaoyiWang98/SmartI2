#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-8-16

import cv2
import numpy as np
from threading import Thread
import datetime
import math
import csv
from IndexMachineM import GenerateDataSet2

class WebcamVideosStream2:
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

class frameGet2:

	def Getframe(self, fvs, face_cascade, close, further,eye_cascade):
		# make X,Y,H,W global
		GXR = 0
		GYR = 0
		GXW = 0
		GXH = 0
		FXR = 0

		# Capture frame-by-frame
		frame = fvs.read()
		frame = self.hisEqulColor(frame)
		cut = 0
		# Our operations on the frame come here
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		eyes = eye_cascade.detectMultiScale(gray, 1.7, 11)
		# 	FXR = x
		for (ex, ey, ew, eh) in eyes:
			FXR = ex
			GXR = ex
			GYR = ey
			GXW = ew
			GXH = eh
			break

		cv2.imshow('frame', frame)
		# if no face detected
		Y = 0;
		H = 0;
		if FXR != 0:
			# Face position is good
			X = math.floor(GXR + (GXW / 2) - (close / 2))
			Y = math.floor(GYR + (GXH / 2) - (3*close / 5))
			H = close
			W = close
			cut = frame[Y:(Y + H), X:(X + W)]
			cv2.imshow("cut", cut)

		return frame, cut, GXR, Y, H

	def hisEqulColor(self,img):
		ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
		channels = cv2.split(ycrcb)
		cv2.equalizeHist(channels[0], channels[0])
		cv2.merge(channels, ycrcb)
		cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
		return img


class frameRun2:
	def __init__(self, device):
		# 0 for internal webcam, 1 for usb webcam
		if device == 0:
			src = 0
			close = 50
			further = 50
		elif device == 1:
			src = 1
			close = 50
			further = 50
		fvs = WebcamVideosStream2(src).start()

		#for arrows (instruction)
		click = cv2.imread("Arrows/click.png")
		Nothing = cv2.imread("Arrows/Nothing.png")
		RClick = cv2.imread("Arrows/Rclick.png")
		stop = cv2.imread("Arrows/stop.png")
		cv2.namedWindow("Arrows")

		face_cascade = cv2.CascadeClassifier('MouthDetector/cascades/haarcascade_mcs_mouth.xml')
		eye_cascade = cv2.CascadeClassifier('MouthDetector/cascades/haarcascade_mcs_mouth.xml')
		var = 1

		#Read index

		cv2.namedWindow("head")

		path = GenerateDataSet2().mkdir()

		index = [0,0,0,0,0,0,0,0]
		#i,middlei,upi,downi,lefti,righti,clicki,Gi

		action = ['/click','/Nothing','/ForceNoOp']

		counter = 0

		while var == 1:
			frame, head, GXR, Y, H = frameGet2().Getframe(fvs, face_cascade, close, further, eye_cascade)

			if GXR != 0 and Y != 0 and H != 0:
				if cv2.waitKey(1) & 0xFF == ord('d'):  # 16.666ms = 1/60hz
					pathi = path + action[index[0]]+ action[index[0]]

					index[index[0]+1] = self.ImgSandP(pathi,index[index[0]+1],head,Y,H)
					counter+=1

			while (counter >= 100):
				cv2.imshow("Arrows",stop)
				if cv2.waitKey(1) & 0xFF == ord('f'):
					index[7] += 1
					index[0] = index[7] % 2
					counter = 0
					break


			if index[0] == 0:
				cv2.imshow("Arrows",click)
			elif index[0] == 1:
				cv2.imshow("Arrows",RClick)


			if cv2.waitKey(1) & 0xFF == ord('q'):  # 16.666ms = 1/60hz
				rows = [(index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7])]
				print(rows)
				with open(path+'/index.csv',"w") as f:
					f_csv = csv.writer(f)
					f_csv.writerows(rows)
				break


		cv2.destroyAllWindows()
		fvs.stop()

	def ImgSandP(self,pathj,index,head,Y,H):
		print(pathj)
		cv2.imwrite(pathj + str(index) + ".jpg", head)
		print(Y, H)
		cv2.imshow('head', head)
		index += 1
		return index

#Uncommand to direct start image capture process
if __name__ == '__main__':
	frameRun2(0)
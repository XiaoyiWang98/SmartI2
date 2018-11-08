#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-8-16


import cv2
import numpy as np
from threading import Thread
import datetime
import math
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

		#Read index

		cv2.namedWindow("head")

		path = GenerateDataSet().mkdir()

		index = [0,0,0,0,0,0,0,0]
		#i,middlei,upi,downi,lefti,righti,clicki,Gi

		action = ['/middle','/up','/down','/left','/right','/click']
		TV = ['/train','Validation']

		while var == 1:
			frame, head, GXR, Y, H = frameGet().Getframe(fvs, face_cascade, close, further, eye_cascade)

			if GXR != 0 and Y != 0 and H != 0:
				if cv2.waitKey(1) & 0xFF == ord('d'):  # 16.666ms = 1/60hz
					if index[7] <= 1000:
						pathi = path + '/train' + action[index[0]]+ action[index[0]]
					elif index[7] > 1000 & index[7] <= 1300:
						pathi = path + '/validation' + action[index[0]]+ action[index[0]]

					index[index[0]+1] = self.ImgSandP(pathi,index[index[0]+1],head,Y,H)

					index[7] += 1
					index[0] = index[7]%5 #change back to 6 later

			if index[0] == 0:
				cv2.imshow("Arrows",middle)
			elif index[0] == 1:
				cv2.imshow("Arrows",up)
			elif index[0] == 2:
				cv2.imshow("Arrows",down)
			elif index[0] == 3:
				cv2.imshow("Arrows",left)
			elif index[0] == 4:
				cv2.imshow("Arrows",right)
			elif index[0] == 5:
				cv2.imshow("Arrows",click)

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
		cv2.imwrite(pathj + str(index) + ".jpg", head)
		print(Y, H)
		cv2.imshow('head', head)
		index += 1
		return index

#Uncommand to direct start image capture process
if __name__ == '__main__':
	frameRun(0)
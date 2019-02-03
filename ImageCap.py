#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-8-16


import cv2
import numpy as np
from threading import Thread
import time
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
		frame = self.hisEqulColor(frame)
		gray = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		ref_x = 0
		FXR = 0

		FX = 0
		FY = 0
		FW = 0
		FH = 0


		for (x, y, w, h) in faces:
			FX = x
			FY = y
			FW = w
			FH = h
			roi_gray = gray[y:y + h, x:x + w]
			roi_color = frame[y:y + h, x:x + w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			FXR = x
			for (ex, ey, ew, eh) in eyes:
				ref_x = ex
				GXR = ex+x
				GYR = ey+y
				GXW = ew
				GXH = eh
				cv2.rectangle(roi_color, (GXR, GYR), (GXR + GXW, GYR + GXH), (0, 255, 0), 2)
				break
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
				cut = self.hisEqulColor(cut)
				cv2.rectangle(roi_color, (X, Y), (X+W, Y+H), (0, 255, 0), 2)

		return frame, cut, GXR, Y, H, FX, FY, FW, FH

	def hisEqulColor(self, img):
		ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
		channels = cv2.split(ycrcb)
		cv2.equalizeHist(channels[0], channels[0])
		cv2.merge(channels, ycrcb)
		cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
		return img


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
		stop = cv2.imread("Arrows/stop.png")
		cv2.namedWindow("Arrows")


		a = cv2.imread("rotating/3.png")
		b = cv2.imread("rotating/4.png")
		c = cv2.imread("rotating/5.png")
		d = cv2.imread("rotating/6.png")
		e = cv2.imread("rotating/7.png")



		face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
		var = 1

		#Read index


		path = GenerateDataSet().mkdir()

		index = [0,0,0,0,0,0,0,0]
		print(path)
		with open(path+'/index.csv') as f:
			f_csv = csv.reader(f)
			for row in f_csv:
				print(int(row[1]))
				for i in range(len(row)):
					index[i] = int(row[i])

		action = ['/up','/down','/left','/right','/click']

		counter = -1
		ind = 0
		SampleEpisode = 10
		roundcounter = 0
		MaxRC = 2
		relaxTime = 5

		t1 = time.clock()

		cut = np.zeros((200, 200 ,3), np.uint8)
		showcut = cv2.resize(cut, (200, 200))
		showarr = np.zeros((200, 200 ,3), np.uint8)

		FXMIN = 1000
		FXMAX = 0

		FYMIN = 1000
		FYMAX = 0

		FWMIN = 1000
		FWMAX = 0

		FHMIN = 1000
		FHMAX = 0

		while var == 1:
			frame, head, GXR, Y, H, FX, FY, FW, FH = frameGet().Getframe(fvs, face_cascade, close, further, eye_cascade)

			print(FX, FY, FW, FH)

			if GXR != 0 and Y != 0 and H != 0:
				FXMAX, FXMIN = self.compare(FX, FXMAX, FXMIN)
				FYMAX, FYMIN = self.compare(FY, FYMAX, FYMIN)
				FWMAX, FWMIN = self.compare(FW, FWMAX, FWMIN)
				FHMAX, FHMIN = self.compare(FX, FHMAX, FHMIN)

				t2 = time.clock()
				if counter == -1:
					counter = 0
				elif counter == 0:
					seconds(relaxTime,showarr,showframe,showcut)
					counter += 1
				elif counter < SampleEpisode+1:
					if (t2 - t1) >= 0.2:
						pathi = path + action[index[0]] + action[index[0]]
						index[index[0]+1], cut = self.ImgSandP(pathi,index[index[0]+1],head,Y,H)
						print(counter)
						counter += 1
						t1 = time.clock()
				elif counter == SampleEpisode+1:
					index[7] += 1
					index[0] = index[7] % 4
					counter += 1
				else:
					if index[0] == 0:
						roundcounter += 1
					counter = 0
					ind = 0
					if roundcounter == MaxRC:
						ind = 2

			cv2.moveWindow('Arrows', 800, 200)

			if index[0] == 0:
				arr = up
			elif index[0] == 1:
				arr = down
			elif index[0] == 2:
				arr = left
			elif index[0] == 3:
				arr = right

			indsap = counter%5
			if indsap == 0:
				sap = a
			elif indsap == 1:
				sap = b
			elif indsap == 2:
				sap = c
			elif indsap == 3:
				sap = d
			elif indsap == 4:
				sap = e

			showarr = cv2.resize(arr, (200,200))
			showframe = cv2.resize(frame, (200, 200))
			showcut = cv2.resize(cut, (200,200))
			showsap = cv2.resize(sap, (200,200))
			numpy_horizontal = np.hstack((showarr,showsap))
			numpy2 = np.hstack((showcut,showframe))
			numpytotal = np.vstack((numpy_horizontal,numpy2))
			cv2.imshow("Arrows",numpytotal)



			if ind == 2:
				rows = [(index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7])]
				print(rows)
				with open(path + '/index.csv', "w") as f:
					f_csv = csv.writer(f)
					f_csv.writerows(rows)

				rows2 = [FXMAX,FXMIN,FYMAX,FYMAX,FWMAX,FWMIN,FHMAX,FHMIN]
				with open(path + '/FacePos.csv', "w") as f2:
					f_csv2 = csv.writer(f2)
					f_csv2.writerows(rows2)

				break

			if cv2.waitKey(1) & 0xFF == ord('q'):  # 16.666ms = 1/60hz
				rows = [(index[0], index[1], index[2], index[3], index[4], index[5], index[6], index[7])]
				print(rows)
				with open(path+'/index.csv',"w") as f:
					f_csv = csv.writer(f)
					f_csv.writerows(rows)

				rows2 = [(FXMAX,FXMIN,FYMAX,FYMIN,FWMAX,FWMIN,FHMAX,FHMIN)]
				with open(path + '/FacePos.csv', "w") as f2:
					f_csv2 = csv.writer(f2)
					f_csv2.writerows(rows2)
				break


		cv2.destroyAllWindows()
		fvs.stop()
		return

	def compare(self, value, Max, Min):
		if value < Min:
			Min = value
		elif value > Max:
			Max = value
		return Max, Min


	def ImgSandP(self,pathj,index,head,Y,H):
		cv2.imwrite(pathj + str(index) + ".jpg", head)
		print()
		index += 1
		return index, head


class seconds:
	def __init__(self,counter, showarr, showframe, showcut):
		one = cv2.imread("numbers/one.png")
		two = cv2.imread("numbers/two.png")
		three = cv2.imread("numbers/three.png")
		four = cv2.imread("numbers/four.png")
		five = cv2.imread("numbers/five.png")
		six = cv2.imread("numbers/six.png")
		seven = cv2.imread("numbers/seven.png")
		eight = cv2.imread("numbers/eight.png")
		nine = cv2.imread("numbers/nine.png")
		ten = cv2.imread("numbers/ten.png")
		zero = cv2.imread("numbers/zero.png")
		big = cv2.imread("Arrows/stop.png")
		t1 = time.clock()
		while counter >= 0:
			t2 = time.clock()
			if t2 - t1 > 0.5:
				t1 = time.clock()
				counter -= 1
			print(counter)
			if counter == 1:
				num = one
			elif counter == 2:
				num = two
			elif counter == 3:
				num = three
			elif counter == 4:
				num = four
			elif counter == 5:
				num = five
			elif counter == 6:
				num = six
			elif counter == 7:
				num = seven
			elif counter == 8:
				num = eight
			elif counter == 9:
				num = nine
			elif counter == 10:
				num = ten
			elif counter == 0:
				num = zero
			elif counter >= 10:
				num = big

			num = cv2.resize(num, (200,200))
			numpy_horizontal = np.hstack((showarr,num))
			numpy2 = np.hstack((showcut,showframe))
			numpytotal = np.vstack((numpy_horizontal,numpy2))
			cv2.imshow("Arrows",numpytotal)
			if cv2.waitKey(1) == ord('q'):
				break

#Uncommand to direct start image capture process
if __name__ == '__main__':
	frameRun(0)

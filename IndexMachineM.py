#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-Oct-30


import cv2
import numpy as np
from threading import Thread
import datetime
import math
import csv
import os
import time


class general:
	def __init__(self):
		i, middlei, upi, downi, lefti, righti, clicki, Gi = self.getlocalIndex()
		print(i, middlei, upi, downi, lefti, righti, clicki, Gi)

	def getlocalIndex(self):
		with open('index.csv', "r") as f:
			print("Index Loaded")
			f_csv = csv.reader(f)
			row = next(f_csv)
			i = int(row[0])
			middlei = int(row[1])
			upi = int(row[2])
			downi = int(row[3])
			lefti = int(row[4])
			righti = int(row[5])
			clicki = int(row[6])
			Gi = int(row[7])
		return i,middlei,upi,downi,lefti,righti,clicki,Gi


#Show all datafolder's in the sample folder with the folder name of timestamp.
#Users can choose which one to be output.
#Save the folders users want to output in the setout folder.

class GenerateDataSet2:
	def __init__(self):
		return

	def mkdir(self):

		DataName = "1000";

		path = "MouthDetector/CurrentData/" + DataName
		folder = os.path.exists(path)

		if not folder:
			os.makedirs(path)
			pathdir = ['/click','/Nothing','/ForceNoOp']
			for j in range(len(pathdir)):
				pathi = path+pathdir[j]
				os.makedirs(pathi)
				with open(path + '/index.csv', 'w') as f:
					f.write('0,0,0,0,0,0,0,0')
			print("---  new folder...  ---")
			print("---  OK  ---")

		else:
			print("---  There is this folder!  ---")

		return path


if __name__ == '__main__':
	path = GenerateDataSet2().mkdir()
	print(path)
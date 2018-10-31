#Sample Collection Back-end
#Xiaoyi(Sean) Wang
#2018-Oct-30


import cv2
import numpy as np
from threading import Thread
import datetime
import math
import csv


class Setin:
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


if __name__ == '__main__':
	Setin()
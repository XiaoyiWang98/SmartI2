# provides the classification result for a single input image

# Siqi Dai
# Jan 8, 2019

from train_model import accessImgPixelVal, train_model
from validate_model import className
import math
import os
import csv
import cv2


# this function will return an index, where:
# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> middle; 5 -> click
def classifySingleImage(img_path):
  # get the model parameters: theta and miu_list
  miu_list, theta = [], 0
  if os.path.isfile('model_param_eyes.csv'):
    i = True
    with open('model_param_eyes.csv', "r") as f:
      f_csv = csv.reader(f)
      for row in f_csv:
        if i:
          theta = float(row[0])
          i = False
        else:
          miu_list.append(row)
    f.close()

  img = cv2.imread(img_path, 0)
  img = cv2.equalizeHist(img)  # histogram equalization
  row, col = img.shape[0], img.shape[1]
  pixel_vals = []
  for i in range(row):
    for j in range(col):
      pixel_vals.append(img[i, j])

  num_of_attribute = len(pixel_vals)

  prob = [1, 1, 1, 1, 1, 1]  # probabilities of predicting different classes: up, down, left, right, middle, click
  for m in range(6):  # 6 possible classes
    expo = 0
    for i in range(0, num_of_attribute):
      expo = expo + int(pixel_vals[i] - float(miu_list[m][i])) ** 2
    expo = (-1 / (2 * (int(theta) ** 2))) * expo
    prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / 6

  if max(prob) < math.exp(-90):
    max_idx = 4  # if max(prob) < some threshold, output "middle"
  else:
    max_idx = prob.index(max(prob))  # max_idx is the prediction result

  print(img_path, ': ', className(max_idx))

  return max_idx


if __name__ == "__main__":
  max_idx = classifySingleImage("down1.jpg")
  # max_idx = classifySingleImage("down2.jpg")
  # max_idx = classifySingleImage("down3.jpg")
  # max_idx = classifySingleImage("down4.jpg")
  # max_idx = classifySingleImage("down5.jpg")
  # max_idx = classifySingleImage("down6.jpg")
  # max_idx = classifySingleImage("down7.jpg")
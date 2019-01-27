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
# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> noPredictionResult; 5 -> click (mouth_open); 6 -> force_eye_noOp
def classifySingleImage(img_path, num_of_classes):
  # get the model parameters: theta and miu_list
  miu_list, theta = [], 0
  fn = 'model_param_eyes.csv' if num_of_classes == 4 else 'model_param_mouth.csv'
  if os.path.isfile(fn):
    i = True
    with open(fn, "r") as f:
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
  prob = [1] * num_of_classes  # probabilities of predicting different classes

  for m in range(num_of_classes):  # for all possible classes
    expo = 0
    for i in range(0, num_of_attribute):
      expo = expo + int(pixel_vals[i] - float(miu_list[m][i])) ** 2
    expo = (-1 / (2 * (int(theta) ** 2))) * expo
    prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / num_of_classes

  if num_of_classes == 4:  # for eyes
    if max(prob) < math.exp(-200):
      idx = 4  # if max(prob) < some threshold, output "noPredictionResult"
    else:
      idx = prob.index(max(prob))
  else:  # for mouth
    if max(prob) < math.exp(-200):  # this threshold: to be decided later
      idx = 4  # if max(prob) < some threshold, output "noPredictionResult"
      print("Nothing")
    else:
      idx = prob.index(max(prob)) + 5
      print("")
  print(img_path, ': ', className(prob.index(max(prob)), num_of_classes))

  return idx


if __name__ == "__main__":
  idx = classifySingleImage("down1.jpg", 4)
  idx = classifySingleImage("click1.jpg", 2)
  #idx = classifySingleImage("click2.jpg", 2)
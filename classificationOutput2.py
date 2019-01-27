# provides the classification result for a single input image

# Siqi Dai (modified by Sean)
# Jan 8, 2019

from train_model import accessImgPixelVal, train_model
from validate_model import className
import math
import os
import csv
import cv2


class classify:
  def classifyInit(self, num_of_classes):
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
    return miu_list, theta

  # this function will return an index, where:
  # 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> noPredictionResult; 5 -> click (mouth_open); 6 -> force_eye_noOp
  def classifySingleImage2(self, img, miu_list, theta, num_of_classes):
    img = cv2.equalizeHist(img)  # histogram equalization
    row, col = img.shape[0], img.shape[1]
    pixel_vals = []
    for i in range(row):
      for j in range(col):
        pixel_vals.append(img[i, j])

    num_of_attribute = len(pixel_vals)
    prob = [1] * num_of_classes

    for m in range(num_of_classes):  # for all possible classes
      expo = 0
      for i in range(0, num_of_attribute):
        expo = expo + int(pixel_vals[i] - float(miu_list[m][i])) ** 2
      expo = (-1 / (2 * (int(theta) ** 2))) * expo
      prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / num_of_classes

    if num_of_classes == 4:  # for eyes
      #print(prob, math.exp(-200))
      if max(prob) < math.exp(-200):
        idx = 4  # if max(prob) < some threshold, output "noPredictionResult"
      else:
        idx = prob.index(max(prob))
      print(className(prob.index(max(prob)), num_of_classes))
    else:  # for mouth
      #print(prob, math.exp(-200))
      if prob.index(max(prob)) + 5 == 5:
        idx = 5
        print("Click")
      else:
        idx = 4
        print("Nothing")

   #print(prob[0], prob[1])
    print(idx)

    return idx


if __name__ == "__main__":
  # miu_list, theta = classify.classifyInit(0, 4)
  # img = cv2.imread("down1.jpg", 0)
  # idx = classify.classifySingleImage2(0, img, miu_list, theta, 4)
  # print(idx)


  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click40.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click41.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click42.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click43.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click44.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click45.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("click46.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing8.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing9.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing10.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing11.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing12.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing13.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)

  miu_list, theta = classify.classifyInit(0, 2)
  img = cv2.imread("Nothing14.jpg", 0)
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 2)
  print(idx)
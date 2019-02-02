# provides the classification result for a single input image

# Siqi Dai (modified by Sean)
# Jan 8, 2019


from validate_model import className
import math
import os
import csv
import cv2
import glob


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
  # 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> click (mouth_open); 5 -> forceNoOp; 6 -> mouth_nothing
  def classifySingleImage2(self, img, miu_list, theta, num_of_classes):
    if num_of_classes == 4:
      img = cv2.equalizeHist(img)  # histogram equalization

    row, col = img.shape[0], img.shape[1]
    pixel_vals = []
    for i in range(row):
      for j in range(col):
        if(num_of_classes == 4):
          pixel_vals.append(img[i, j])
        else:
          pixel_vals.append(img[i, j, 0])

    num_of_attribute = len(pixel_vals)
    prob = [1] * num_of_classes

    for m in range(num_of_classes):  # for all possible classes
      expo = 0
      for i in range(0, num_of_attribute):
        expo = expo + int(pixel_vals[i] - float(miu_list[m][i])) ** 2
      expo = (-1 / (2 * (int(theta) ** 2))) * expo
      prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / num_of_classes

    if num_of_classes == 4:  # for eyes
      #if max(prob) < threshold_eye:
      #if max(prob) < math.exp(-300):
      #  idx = 4  # if max(prob) < some threshold, output "noPredictionResult"
      #else:
      idx = prob.index(max(prob))
    else:  # for mouth
      idx = prob.index(max(prob)) + 4

    print(idx, className(prob.index(max(prob)), num_of_classes))
    # print(prob)

    return idx


  # returns the threshold for eye images
  def tuneThreshold(self, miu_list, theta):
    threshold_eye = 0
    path_eye = "./TestThreshold/"

    img_eye = [cv2.imread(f, 0) for f in glob.glob(path_eye + '*.jpg')]

    classify_eye, probs = [], []
    for img in img_eye:
      idx, prob = classify.classifySingleImage2(0, img, miu_list, theta, 4, threshold_eye)
      classify_eye.append(idx)
      probs = probs + prob

    count_error_eye = sum(1 for x in classify_eye if x != 4)
    i = min(prob)/2  # learning rate

    while count_error_eye != 0:
      classify_eye = []
      threshold_eye = threshold_eye + i
      for img in img_eye:
        idx, prob = classify.classifySingleImage2(0, img, miu_list, theta, 4, threshold_eye)
        classify_eye.append(idx)
      count_error_eye = sum(1 for x in classify_eye if x != 4)
      #print(count_error_eye)

    return threshold_eye


if __name__ == "__main__":

  # miu_listE, thetaE = classify.classifyInit(0, 4)
  # threshold = classify.tuneThreshold(0, miu_listE, thetaE)
  # print(threshold)
  #
  # img = cv2.imread("middle5.jpg", 0)
  # idx = classify.classifySingleImage2(0, img, miu_listE, thetaE, 4)


  miu_list, theta = classify.classifyInit(0, 3)

  img = cv2.imread("click0.jpg")
  idx = classify.classifySingleImage2(0, img, miu_list, theta, 3)


# train the model using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018

import glob
import cv2
import math
import csv
from multiprocessing.pool import ThreadPool


def train_model(percent, info, num_of_classes):
  # percent = % of training data in the dataset;
  # info: 1 -> print data info; 0 -> not print data info;
  # num_of_classes (total number of classes for an object): 4 -> eye; 2 -> mouth

  train_set, valid_set = getImageSets(percent, info, num_of_classes)

  # access pixel values of the images in the respective folders
  train_data = []
  flag = 1

  for train in train_set:
    pixels = accessImgPixelVal(train, num_of_classes)
    train_data.append(pixels)
    if len(train) == 0:
      flag = 0

  if flag == 1:  # there are training images for all classes
    miu_list = computeMiu(train_data, num_of_classes)  # miu
    theta = computeTheta(train_data, miu_list, num_of_classes)  # shared vector theta (pixel noise standard deviation)
    if info == 1:
      print('Prediction model was successfully built! Press the "Testing" button.\n')

    # save the model parameters in a csv file
    fn = 'model_param_eyes.csv' if num_of_classes == 4 else 'model_param_mouth.csv'
    writeModelParamInCSV(fn, theta, miu_list)

  else:  # missing training images for at least one class
    miu_list, theta = [], 0
    if info == 1:
      print('Missing training data for at least one class.\n')

  return miu_list, theta


def accessImgPixelVal(imgset, num_of_classes):
  list = []
  if len(imgset) != 0:
    for im in imgset:
      if num_of_classes == 4:  # for eyes
        img = cv2.imread(im, 0)
        img = cv2.equalizeHist(img)  # histogram equalization
      else:  # for mouth
        img = cv2.imread(im)

      row, col = img.shape[0], img.shape[1]
      if num_of_classes == 4:  # for eyes
        pixel_vals = [img[i, j] for i in range(row) for j in range(col)]
      else:  # for mouth
        pixel_vals = [img[i, j, 0] for i in range(row) for j in range(col)]
      list.append(pixel_vals)

  return list


# compute the vector miu
def computeMiu(train_data, num_of_classes):
  miu_list = []
  for k in range(0, num_of_classes):
    num_of_attribute = len(train_data[k][0])
    num_imgs = len(train_data[k])
    miu = []
    for i in range(0, num_of_attribute):
      x_kji = 0
      for j in range(num_imgs):
        x_kji = x_kji + train_data[k][j][i]
      miu.append(x_kji / num_imgs)
    miu_list.append(miu)
  return miu_list


# compute the shared vector theta (pixel noise standard deviation)
def computeTheta(train_data, miu_list, num_of_classes):
  sum = 0
  num_of_attribute = len(train_data[0][0])
  for k in range(0, num_of_classes):
    for j in range(0, len(train_data[k])):
      for i in range(0, num_of_attribute):
        sum = sum + (train_data[k][j][i] - miu_list[k][i])**2
  theta = math.sqrt(sum/num_of_attribute/len(train_data[k]))
  return theta


def split(list, percent):  # split a list into two sub-lists
  length = int(len(list) * percent / 100)
  sublist1 = [list[i] for i in range(length)]
  sublist2 = [list[i] for i in range(length, len(list))]
  return sublist1, sublist2


def getImageSets(percent, info, num_of_classes):  # get train and validation image sets
  data_path = './CurrentData/' if num_of_classes == 4 else './MouthDetector/CurrentData/'
  # read csv
  file = open(data_path + 'Dataset.csv')
  contents = file.readlines()
  folders = []
  for i in range(len(contents)):
    if contents[i] != "\n":
      folders.append(contents[i].rstrip("\n"))

  if num_of_classes == 4:  # for eye images
    up, down, left, right = [], [], [], []
    for file in folders:
      img_path = data_path + file + '/'
      up = up + [f for f in glob.glob(img_path + 'up/' + '*.jpg')]
      down = down + [f for f in glob.glob(img_path + 'down/' + '*.jpg')]
      left = left + [f for f in glob.glob(img_path + 'left/' + '*.jpg')]
      right = right + [f for f in glob.glob(img_path + 'right/' + '*.jpg')]
    train_up, valid_up = split(up, percent)
    train_down, valid_down = split(down, percent)
    train_left, valid_left = split(left, percent)
    train_right, valid_right = split(right, percent)

    if info == 1:  # print information
      print('Total Number of Data: \n   up: ', len(up), '; down: ', len(down), '; left: ', len(left), '; right: ',
            len(right))
      print('Number of Training Data: \n   up: ', len(train_up), '; down: ', len(train_down), '; left: ',
            len(train_left), '; right: ', len(train_right))
      print('Number of Test Data: \n   up: ', len(valid_up), '; down: ', len(valid_down), '; left: ', len(valid_left),
            '; right: ', len(valid_right))

    train_set = [train_up, train_down, train_left, train_right]
    valid_set = [valid_up, valid_down, valid_left, valid_right]

  else:  # for mouth images
    mouth_open, mouth_line, mouth_nothing = [], [], []
    for file in folders:
      img_path = data_path + file + '/'
      mouth_open = mouth_open + [f for f in glob.glob(img_path + 'click/' + '*.jpg')]
      mouth_line = mouth_line + [f for f in glob.glob(img_path + 'ForceNoOp/' + '*.jpg')]
      mouth_nothing = mouth_nothing + [f for f in glob.glob(img_path + 'nothing/' + '*.jpg')]
    train_mouth_open, valid_mouth_open = split(mouth_open, percent)
    train_mouth_line, valid_mouth_line = split(mouth_line, percent)
    train_mouth_nothing, valid_mouth_nothing = split(mouth_nothing, percent)

    if info == 1:  # print information
      print('Total Number of Data: \n   mouth_open: ', len(mouth_open), '; mouth_force_no_op: ', len(mouth_line),
            '; mouth_nothing: ', len(mouth_nothing))
      print('Number of Training Data: \n   mouth_open: ', len(train_mouth_open), '; mouth_force_no_op: ',
            len(train_mouth_line), '; mouth_nothing: ', len(train_mouth_nothing))
      print('Number of Test Data: \n   mouth_open: ', len(valid_mouth_open), '; mouth_force_no_op: ',
            len(valid_mouth_line), '; mouth_nothing: ', len(valid_mouth_nothing))

    train_set = [train_mouth_open, train_mouth_line, train_mouth_nothing]
    valid_set = [valid_mouth_open, valid_mouth_line, valid_mouth_nothing]

  return train_set, valid_set


def writeModelParamInCSV(fn, theta, miu_list):
  with open(fn, "w") as write_f:
    writer = csv.writer(write_f)
    writer.writerow([theta])
    writer.writerows(miu_list)
  write_f.close()
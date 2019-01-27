# train the model using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018

import glob
import cv2
import math
import csv


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
      pixel_vals = []
      for i in range(row):
        for j in range(col):
          if num_of_classes == 4:  # for eyes
            pixel_vals.append(img[i, j])
          else:  # for mouth
            pixel_vals.append(img[i, j, 0])
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
  sublist1, sublist2 = [], []
  length = int(len(list) * percent / 100)
  for i in range(length):
    sublist1.append(list[i])
  for i in range(length, len(list)):
    sublist2.append(list[i])
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
      for f in glob.glob(img_path + 'up/' + '*.jpg'):
        up.append(f)
      for f in glob.glob(img_path + 'down/' + '*.jpg'):
        down.append(f)
      for f in glob.glob(img_path + 'left/' + '*.jpg'):
        left.append(f)
      for f in glob.glob(img_path + 'right/' + '*.jpg'):
        right.append(f)
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
    mouth_open, mouth_line = [], []
    for file in folders:
      img_path = data_path + file + '/'
      for f in glob.glob(img_path + 'click/' + '*.jpg'):
        mouth_open.append(f)  # left click
      for f in glob.glob(img_path + 'ForceNoOp/' + '*.jpg'):
        mouth_line.append(f)  # force_no_op
    train_mouth_open, valid_mouth_open = split(mouth_open, percent)
    train_mouth_line, valid_mouth_line = split(mouth_line, percent)

    if info == 1:  # print information
      print('Total Number of Data: \n   mouth_open: ', len(mouth_open), '; mouth_force_no_op: ', len(mouth_line))
      print('Number of Training Data: \n   mouth_open: ', len(train_mouth_open), '; mouth_force_no_op: ',
            len(train_mouth_line))
      print('Number of Test Data: \n   mouth_open: ', len(valid_mouth_open), '; mouth_force_no_op: ',
            len(valid_mouth_line))

    train_set = [train_mouth_open, train_mouth_line]
    valid_set = [valid_mouth_open, valid_mouth_line]

  return train_set, valid_set


def writeModelParamInCSV(fn, theta, miu_list):
  with open(fn, "w") as write_f:
    writer = csv.writer(write_f)
    writer.writerow([theta])
    writer.writerows(miu_list)
  write_f.close()
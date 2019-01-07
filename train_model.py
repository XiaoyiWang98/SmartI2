# train the model using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018

import glob
import cv2
import math
import csv


def train_model(percent, info):  # percent = % of training data in the dataset
  train_set, valid_set = getImageSets(percent, info)

  # access the pixel values and the total number of images in the respective folders
  train_data = []
  flag = 1
  i = 0
  for train in train_set:
    i = i+1
    pixels = accessImgPixelVal(train)
    train_data.append(pixels)
    if len(train) == 0:
      flag = 0

  if flag == 1:  # there are images in all training classes
    miu_list = computMiu(train_data)
    theta = computeTheta(train_data, miu_list)  # shared vector theta (pixel noise standard deviation)
    if info == 1:
      print('Prediction model was successfully built! Press the "testing" button.\n')
  else:
    miu_list = []
    theta = 0
    if info == 1:
      print('There missing training data for at least one class.\n')

  return miu_list, theta, valid_set


def accessImgPixelVal(imgset):
  list = []
  if len(imgset) != 0:
    for im in imgset:
      img = cv2.imread(im,0)
      img = cv2.equalizeHist(img)  # histogram equalization
      #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
      row, col = img.shape[0], img.shape[1]
      pixel_vals = []
      for i in range(row):
        for j in range(col):
          pixel_vals.append(img[i, j])
      list.append(pixel_vals)
  return list


# compute the vector miu
def computMiu(train_data):
  miu_list = []
  for k in range(0, 6):  # six classes
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
def computeTheta(train_data, miu_list):
  sum = 0
  num_of_attribute = len(train_data[0][0])
  for k in range(0, 6):
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


def getImageSets(percent, info):  # get train and validation image sets
  # read csv
  data_path = './CurrentData/'
  file = open(data_path + 'Dataset.csv')
  contents = file.readlines()
  folders = []
  for i in range(len(contents)):
    if contents[i] != "\n":
      folders.append(contents[i].rstrip("\n"))

  up, down, left, right, middle, click = [], [], [], [], [], []
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
    for f in glob.glob(img_path + 'middle/' + '*.jpg'):
      middle.append(f)
    for f in glob.glob(img_path + 'click/' + '*.jpg'):
      click.append(f)

  train_up, valid_up = split(up, percent)
  train_down, valid_down = split(down, percent)
  train_left, valid_left = split(left, percent)
  train_right, valid_right = split(right, percent)
  train_middle, valid_middle = split(middle, percent)
  train_click, valid_click = split(click, percent)

  if info == 1:  # print information
    print('Total Number of Data: \n   up: ', len(up), '; down: ',len(down), '; left: ',len(left),
          '; right: ', len(right), '; middle: ', len(middle), '; click: ', len(click), '\n')
    print('Number of Training Data: \n   up: ', len(train_up), '; down: ',len(train_down), '; left: ',len(train_left),
          '; right: ', len(train_right), '; middle: ', len(train_middle), '; click: ', len(train_click), '\n')
    print('Number of Test Data: \n   up: ', len(valid_up), '; down: ', len(valid_down), '; left: ', len(valid_left),
          '; right: ', len(valid_right), '; middle: ', len(valid_middle), '; click: ', len(valid_click), '\n')

  train_set = [train_up, train_down, train_left, train_right, train_middle, train_click]
  valid_set = [valid_up, valid_down, valid_left, valid_right, valid_middle, valid_click]

  return train_set, valid_set


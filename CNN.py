import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from DataPreprocessing import preprocess
import glob
import cv2
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.utils import to_categorical


# 0 -> up; 1 -> down; 2 -> left; 3 -> right; 4 -> click (mouth_open); 5 -> forceNoOp; 6 -> mouth_nothing
def CNNModel(percent, info, num_of_classes, channels):
  train_img, valid_img, label_train, label_valid = getImageSets(percent, info, num_of_classes)

  train, width, height = imgToArray(train_img, 1)
  valid, width, height = imgToArray(valid_img, 1)
  train = train.reshape(len(train_img), width, height, channels)
  valid = valid.reshape(len(valid_img), width, height, channels)
  label_train = to_categorical(label_train)
  label_valid = to_categorical(label_valid)

  model = Sequential()
  model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=[width, height, channels]))
  model.add(Conv2D(32, (3, 3), activation='relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Flatten())
  model.add(Dense(num_of_classes, activation='softmax'))

  model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
  model.fit(train, label_train, validation_data=(valid, label_valid), epochs=3)


def imgToArray(imgset, channels):
  img = cv2.imread(imgset[0], 0)
  height, width = img.shape[0], img.shape[1]

  all_images = []
  for f in imgset:
    img = cv2.imread(f, 0)  # greyscale
    img = img.reshape([width, height])
    all_images.append(img)
  set = np.array(all_images)

  return set, width, height


def split(list, percent):  # split a list into two sub-lists
  length = int(len(list) * percent / 100)
  sublist1 = [list[i] for i in range(length)]
  sublist2 = [list[i] for i in range(length, len(list))]
  return sublist1, sublist2


def getImageSets(percent, info, num_of_classes):  # get train and validation image sets
  thresh = 1.5  # threshold for outliers

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

      preprocess(img_path + 'up/', thresh)
      preprocess(img_path + 'down/', thresh)
      preprocess(img_path + 'left/', thresh)
      preprocess(img_path + 'right/', thresh)

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


    # data augmentation
    
    train_set = train_up + train_down + train_left + train_right
    label_train_set = [0]*len(train_up) + [1]*len(train_down) + [2]*len(train_left) + [3]*len(train_right)
    valid_set = valid_up + valid_down + valid_left + valid_right
    label_valid_set = [0] * len(valid_up) + [1] * len(valid_down) + [2] * len(valid_left) + [3] * len(valid_right)

  else:  # for mouth images
    mouth_open, mouth_line, mouth_nothing = [], [], []
    for file in folders:
      img_path = data_path + file + '/'

      preprocess(img_path + 'click/', thresh)
      preprocess(img_path + 'ForceNoOp/', thresh)
      preprocess(img_path + 'nothing/', thresh)

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

    train_set = train_mouth_open + train_mouth_line + train_mouth_nothing
    label_train_set = [0] * len(train_mouth_open) + [1] * len(train_mouth_line) + [2] * len(train_mouth_nothing)
    valid_set = valid_mouth_open + valid_mouth_line + valid_mouth_nothing
    label_valid_set = [0] * len(valid_mouth_open) + [1] * len(valid_mouth_line) + [2] * len(valid_mouth_nothing)

  return train_set, valid_set, np.array(label_train_set), np.array(label_valid_set)



if __name__ == "__main__":
  CNNModel(90,1, 4,1)

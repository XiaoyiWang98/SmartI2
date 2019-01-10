# predict the output using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018


from train_model import accessImgPixelVal, getImageSets
import glob
import math
import os
import csv


def validate_model(percent, info, num_of_classes):
  train_set, valid_set = getImageSets(percent, info, num_of_classes)

  # get model parameters
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

  print('===============================\n\nPrediction results:\n')
  flag = 1
  validation_data = []
  for validation in valid_set:
    pixels = accessImgPixelVal(validation)
    validation_data.append(pixels)
    if len(validation) == 0:
      flag = 0

  if flag == 1:
    num_of_attribute = len(validation_data[0][0])
    if num_of_classes == 4:  # for eyes
      prediction_result, accuracy = [0, 0, 0, 0], [0, 0, 0, 0]
    else:  # for mouth
      prediction_result, accuracy = [0, 0, 0], [0, 0, 0]

    for k in range(0, num_of_classes):
      print('validation file "', className(k), '": ')
      error_case = 0  # count the number of incorrectly predicted cases
      for j in range(len(validation_data[k])):
        prob = [1, 1, 1, 1] if num_of_classes == 4 else [1, 1, 1]  # probabilities of predicting different classes
        for m in range(num_of_classes):  # for all possible classes
          expo = 0
          for i in range(0, num_of_attribute):
            expo = expo + int(validation_data[k][j][i] - float(miu_list[m][i])) ** 2
          expo = (-1 / (2 * (int(theta) ** 2))) * expo
          prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / num_of_classes
        max_idx = prob.index(max(prob))  # max_idx is the prediction result
        print('  ', className(max_idx))
        if max_idx != k:
          error_case = error_case + 1
      prediction_result[k] = error_case
      print('===================')

    for i in range(num_of_classes):
        accuracy[i] = (1 - prediction_result[i] / len(valid_set[i])) * 100

    formated_accuracy = [float('%.2f' % elem) for elem in accuracy]
    if num_of_classes == 4:  # for eyes
      print('Number of error cases for up, down, left, right:\n   ', prediction_result, '\n')
      print('Prediction accuracy for up, down, left, right (%):\n   ', formated_accuracy, '\n')
    else:  # for mouth
      print('Number of error cases for mouth_open, mouth_normal_state, mouth_line:\n   ', prediction_result, '\n')
      print('Prediction accuracy for mouth_open, mouth_normal_state, mouth_line (%):\n   ', formated_accuracy, '\n')

  else:
    print('There are no test images for at least one class!\n')


def className(m):
  if m == 0:
    return 'up'
  elif m == 1:
    return 'down'
  elif m == 2:
    return 'left'
  elif m == 3:
    return 'right'
  elif m == 4:
    return 'mouth_open'
  elif m == 5:
    return 'mouth_normal'
  elif m == 6:
    return 'mouth_line'
  else:
    return 'noOp'  # no operation, same as "middle"
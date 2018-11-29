# predict the output using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018


from train_model import accessImgPixelVal, train_model
import glob
import math

def validate_model(percent, info):
  miu_list, theta, valid_set = train_model(percent, info)

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

    prediction_result = [0, 0, 0, 0, 0, 0]
    accuracy = [0, 0, 0, 0, 0, 0]
    for k in range(0, 6):
        print('validation file "', className(k), '": ')
        error_case = 0  # count the number of incorrectly predicted cases
        for j in range(len(validation_data[k])):
            prob = [1, 1, 1, 1, 1, 1]  # probabilities of predicting different classes: up, down, left, right, middle, click
            for m in range(6):  # 6 possible classes
                expo = 0
                for i in range(0, num_of_attribute):
                    expo = expo + int(validation_data[k][j][i] - miu_list[m][i]) ** 2
                expo = (-1 / (2 * (int(theta) ** 2))) * expo
                prob[m] = math.pow(2 * math.pi * theta ** 2, -num_of_attribute / 200) * math.exp(expo) / 6

            max_idx = prob.index(max(prob))  # max_idx is the prediction result
            print('  ', className(max_idx))
            if max_idx != k:
                error_case = error_case + 1
        prediction_result[k] = error_case
        print('===================')

    for i in range(6):
        accuracy[i] = (1 - prediction_result[i] / len(valid_set[i])) * 100

    formated_accuracy = [float('%.2f' % elem) for elem in accuracy]
    print('Number of error cases for up, down, left, right, middle, click:\n   ', prediction_result, '\n')
    print('Prediction accuracy for up, down, left, right, middle, click (%):\n   ', formated_accuracy, '\n')

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
    return 'middle'
  else:
    return 'click'
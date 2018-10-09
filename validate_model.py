# predict the output using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018


from train_model import miu_list, theta, accessImgPixelVal
import glob
import math

def validate():
    print('Prediction results:')
    validation_path = './Samples/validation/'

    imgset_valid_up = glob.glob(validation_path + 'up/' + '*.jpg')
    imgset_valid_down = glob.glob(validation_path + 'down/' + '*.jpg')
    imgset_valid_left = glob.glob(validation_path + 'left/' + '*.jpg')
    imgset_valid_right = glob.glob(validation_path + 'right/' + '*.jpg')
    imgset_valid_middle = glob.glob(validation_path + 'middle/' + '*.jpg')
    imgset_valid_click = glob.glob(validation_path + 'click/' + '*.jpg')

    pixel_valid_up = accessImgPixelVal(imgset_valid_up)
    pixel_valid_down = accessImgPixelVal(imgset_valid_down)
    pixel_valid_left = accessImgPixelVal(imgset_valid_left)
    pixel_valid_right = accessImgPixelVal(imgset_valid_right)
    pixel_valid_middle = accessImgPixelVal(imgset_valid_middle)
    pixel_valid_click = accessImgPixelVal(imgset_valid_click)

    validation_data = [pixel_valid_up, pixel_valid_down, pixel_valid_left, pixel_valid_right, pixel_valid_middle, pixel_valid_click]

    test_images_per_class = 2  # this will be changed! should be at least test images in each folder
    num_of_attribute = len(validation_data[0][0])

    prediction_result = [0, 0, 0, 0, 0, 0]
    for k in range(0, 6):
        print('validation file "', className(k), '": ')
        error_case = 0  # count the number of incorrectly predicted cases
        for j in range(test_images_per_class):
            prob = [1, 1, 1, 1, 1, 1]  # probabilities of predicting different classes: up, down, left, right, middle, click
            for m in range(6):  # 6 possible classes
                expo = 0
                for i in range(0, num_of_attribute):
                    expo = expo + int(validation_data[k][j][i] - miu_list[m][i])**2
                expo = (-1/(2*(int(theta)**2))) * expo
                prob[m] = math.pow(int(2*math.pi*int(theta)**2), int(-num_of_attribute/2)) * math.exp(int(expo)) / 6
            max_idx = prob.index(max(prob))  # max_idx is the prediction result
            print('  ',className(max_idx))
            if(max_idx != k):
                error_case = error_case + 1
        prediction_result[k] = error_case
        print('===================')
    print('Number of error cases for up, down, left, right, middle, click:', prediction_result)


def className(m):
    if (m == 0):
        return 'up'
    elif (m == 1):
        return 'down'
    elif (m == 1):
        return'left'
    elif (m == 1):
        return'right'
    elif (m == 1):
        return'middle'
    else:
        return'click'


if __name__ == "__main__":
    validate()


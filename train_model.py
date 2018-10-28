# train the model using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018

import glob
import cv2
import math


def train_model():
    train_path = './Samples/train/'
    validation_path = './Samples/validation/'

    imgset_train_up = glob.glob(train_path + 'up/' + '*.jpg')
    imgset_train_down = glob.glob(train_path + 'down/' + '*.jpg')
    imgset_train_left = glob.glob(train_path + 'left/' + '*.jpg')
    imgset_train_right = glob.glob(train_path + 'right/' + '*.jpg')
    imgset_train_middle = glob.glob(train_path + 'middle/' + '*.jpg')
    imgset_train_click = glob.glob(train_path + 'click/' + '*.jpg')

    if len(imgset_train_up)!= 0 and len(imgset_train_down)!= 0 and len(imgset_train_left)!= 0 and len(imgset_train_right)!= 0 and len(imgset_train_middle)!= 0 and len(imgset_train_click)!= 0:
        # access the pixel values and the total number of images in the respective folders
        pixel_train_up = accessImgPixelVal(imgset_train_up)
        pixel_train_down = accessImgPixelVal(imgset_train_down)
        pixel_train_left = accessImgPixelVal(imgset_train_left)
        pixel_train_right = accessImgPixelVal(imgset_train_right)
        pixel_train_middle = accessImgPixelVal(imgset_train_middle)
        pixel_train_click = accessImgPixelVal(imgset_train_click)

        train_data = [pixel_train_up, pixel_train_down, pixel_train_left, pixel_train_right, pixel_train_middle, pixel_train_click]
        miu_list = computMiu(train_data)
        theta = computeTheta(train_data, miu_list) # shared vector theta (pixel noise standard deviation)
        print('Prediction model was successfully built! Press the "testing" button.')

    else:
        miu_list = []
        theta = 0

    return miu_list, theta


def accessImgPixelVal(imgset):
    list = []
    if(len(imgset) != 0):
        for im in imgset:
            img = cv2.imread(im)
            row, col = img.shape[0], img.shape[1]
            pixel_vals = []
            for i in range(0,row):
                for j in range(0,col):
                    pixel_vals.append(img[i, j][0]) # only focus on red channel here
            list.append(pixel_vals)
    return list


# compute the vector miu
def computMiu(train_data):
    miu_list = []
    for k in range(0, 6): # six classes
        num_of_attribute = len(train_data[k][0])
        num_imgs = len(train_data[k])
        miu = []
        for i in range(0, num_of_attribute):
            x_kji = 0;
            for j in range(num_imgs):
                x_kji = x_kji + train_data[k][j][i]
            miu.append(x_kji / num_imgs)
        miu_list.append(miu)
    return miu_list


# compute the shared vector theta (pixel noise standard deviation)
def computeTheta(train_data, miu_list):
    sum = 0
    train_images_per_class = 20 # this will be changed! should be at least 100 train images in each folder
    num_of_attribute = len(train_data[0][0])
    for k in range(0, 6):
        for j in range (0, train_images_per_class):
            for i in range(0, num_of_attribute):
                sum = sum + (train_data[k][j][i] - miu_list[k][i])**2
    theta = math.sqrt(sum/num_of_attribute/train_images_per_class)
    return theta


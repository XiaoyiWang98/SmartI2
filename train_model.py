# train the model using conditional Gaussian Classifiers
# note: class label for up, down, left, right, middle， click are 0,1,2,3,4,5 respectively


# Siqi Dai
# Oct 8, 2018

import glob
import cv2
import numpy as np

def train_model():
    train_path = './Samples/train/'
    validation_path = './Samples/validation/'

    imgset_train_up = glob.glob(train_path + 'up/' + '*.jpg')
    imgset_train_down = glob.glob(train_path + 'down/' + '*.jpg')
    imgset_train_left = glob.glob(train_path + 'left/' + '*.jpg')
    imgset_train_right = glob.glob(train_path + 'right/' + '*.jpg')
    imgset_train_middle = glob.glob(train_path + 'middle/' + '*.jpg')
    imgset_train_click = glob.glob(train_path + 'click/' + '*.jpg')

    imgset_valid_up = glob.glob(validation_path + 'up/' + '*.jpg')
    imgset_valid_down = glob.glob(validation_path + 'down/' + '*.jpg')
    imgset_valid_left = glob.glob(validation_path + 'left/' + '*.jpg')
    imgset_valid_right = glob.glob(validation_path + 'right/' + '*.jpg')
    imgset_valid_middle = glob.glob(validation_path + 'middle/' + '*.jpg')
    imgset_valid_click = glob.glob(validation_path + 'click/' + '*.jpg')

    # access the pixel values and the total number of images in the respective folders
    [pixel_train_up, len_train_up], [pixel_valid_up, len_test_up] = accessImgPixelVal(imgset_train_up), accessImgPixelVal(imgset_valid_up)
    [pixel_train_down, len_train_down], [pixel_valid_down, len_test_down] = accessImgPixelVal(imgset_train_down), accessImgPixelVal(imgset_valid_down)
    [pixel_train_left, len_train_left], [pixel_valid_left, len_test_left] = accessImgPixelVal(imgset_train_left), accessImgPixelVal(imgset_valid_left)
    [pixel_train_right, len_train_right], [pixel_valid_right, len_test_right] = accessImgPixelVal(imgset_train_right), accessImgPixelVal(imgset_valid_right)
    [pixel_train_middle, len_train_middle], [pixel_valid_middle, len_test_middle] = accessImgPixelVal(imgset_train_middle), accessImgPixelVal(imgset_valid_middle)
    [pixel_train_click, len_train_click], [pixel_valid_click, len_test_click] = accessImgPixelVal(imgset_train_click), accessImgPixelVal(imgset_valid_click)

    train_data = [pixel_train_up, pixel_train_down, pixel_train_left, pixel_train_right, pixel_train_middle, pixel_train_click]

    print(train_data[0][0])
    print('=====')
    print(pixel_train_up[0])
    print('------------\n')
    print(pixel_train_up[0][1])
    computMiu(pixel_train_up, len_train_up)

def accessImgPixelVal(imgset):
    list = []
    for im in imgset:
        img = cv2.imread(im)
        row, col = img.shape[0], img.shape[1]
        pixel_vals = []
        for i in range(0,row):
            for j in range(0,col):
                pixel_vals.append(img[i, j][0]) # only focus on red channel here
        list.append(pixel_vals)
    return list, len(imgset)

# compute the vector miu
def computMiu(train_data):
    miu = []
    num_of_attribute = len(train_data[0][0])
    for i in range(0, num_of_attribute):
        x_kji = 0;
        for j in range(num_train_imgs):
            x_kji = x_kji + pix_train_data[j][i]




if __name__ == "__main__":
    train_model()


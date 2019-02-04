# data pre-processing: detect wrong samples
# Siqi Dai
# Feb 3, 2019

import os
import glob
import cv2
import numpy as np


def preprocess(path, threshold):
  img_to_delete = []
  if os.path.exists(path):
    imgset = [f for f in glob.glob(path + '*.jpg')]

    pixel_list = []
    for f in imgset:
      img = cv2.imread(f, 0)
      row, col = img.shape[0], img.shape[1]
      pixels = [img[i, j] for i in range(row) for j in range(col)]
      pixel_list.append(pixels)
    pixel_list = np.asarray(pixel_list)

    median = np.median(pixel_list, axis=0)
    diff = np.sum((pixel_list - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / abs_deviation

    img_idx_to_delete = []
    for i in range(len(modified_z_score)):
      if modified_z_score[i] > threshold:
        img_idx_to_delete.append(i)

    img_to_delete = [imgset[i] for i in img_idx_to_delete]

    # delete files
    # for i in img_to_delete:
    #   os.remove(i)

  return img_to_delete


if __name__ == '__main__':
  set = preprocess("./MouthDetector/CurrentData/1000/click/", 1.5)
  print(set)
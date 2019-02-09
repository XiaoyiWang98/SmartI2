# data pre-processing: detect wrong samples
# Siqi Dai
# Feb 3, 2019

import os
import glob
import cv2
import numpy as np
import random
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
import numpy as np


# delete bad samples
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
    for i in img_to_delete:
      os.remove(i)
  return img_to_delete



def random_rotation(image_array: ndarray):
  # pick a random degree of rotation between 25% on the left and 25% on the right
  random_degree = random.uniform(-25, 25)
  return sk.transform.rotate(image_array, random_degree)


def random_noise(image_array: ndarray):
  # add random noise to the image
  return sk.util.random_noise(image_array)


def random_translate(image_array: ndarray):
  tx = random.uniform(-5, 5)
  ty = random.uniform(-5, 5)
  tform = sk.transform.SimilarityTransform(scale=1, rotation=0, translation=(tx, ty))
  rotated = sk.transform.warp(image_array, tform)
  back_rotated = sk.transform.warp(rotated, tform.inverse)
  return back_rotated


def dataAugmentation(folder_path, num_files_desired):
  # loop on all files of the folder and build a list of files paths
  if os.path.exists(folder_path):
    images = [f for f in glob.glob(folder_path + '*.jpg')]

  num_generated_files = 0

  while num_generated_files <= num_files_desired:
    # random image from the folder
    image_path = random.choice(images)
    # read image as an two dimensional array of pixels
    image_to_transform = sk.io.imread(image_path)

    # dictionary of the transformations functions we defined earlier
    available_transformations = {
      'rotate': random_rotation,
      'noise': random_noise,
      'translate': random_translate
    }

    # random num of transformations to apply
    num_transformations_to_apply = random.randint(1, len(available_transformations))

    num_transformations = 0
    transformed_image = None
    while num_transformations <= num_transformations_to_apply:
      # choose a random transformation to apply for a single image
      key = random.choice(list(available_transformations))
      transformed_image = available_transformations[key](image_to_transform)
      num_transformations += 1

    # define a name for the new file
    new_file_path = '%s/augmented_img_%s.jpg' % (folder_path, num_generated_files)

    # write image to the disk
    sk.io.imsave(new_file_path, transformed_image)

    num_generated_files = num_generated_files + 1


if __name__ == '__main__':
  set = preprocess("./MouthDetector/CurrentData/1000/click/", 1.5)

  #dataAugmentation("./MouthDetector/CurrentData/1000/click/", 10)
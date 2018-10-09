# predict the output using conditional Gaussian Classifiers

# Siqi Dai
# Oct 8, 2018


from train_model import miu_list, theta, accessImgPixelVal
import glob

def validate():
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




if __name__ == "__main__":
    validate()


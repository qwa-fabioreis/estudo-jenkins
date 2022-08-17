import cv2
import operator
import numpy as np
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def image_to_black_white(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_inv = cv2.bitwise_not(img_gray)
    img_inv = increase_contrast_brightness(img_inv)

    return img_inv


def text_inversion(img):
    img_inv = cv2.bitwise_not(img)
    image_without_alpha = img_inv.copy()[:, :, :3]
    d_cores = {}

    for line in image_without_alpha:
        for color in line:
            if tuple(color) in d_cores:
                d_cores[tuple(color)]+=1
            else:
                d_cores[tuple(color)]=1


def remove_background(img_inv):

    image_without_alpha = img_inv.copy()
    d_cores = {}

    for color in image_without_alpha:
            if tuple(color) in d_cores:
                d_cores[tuple(color)] += 1
            else:
                d_cores[tuple(color)] = 1

    fundo = max(d_cores.items(), key=operator.itemgetter(1))[0]
    image_without_alpha[np.all(image_without_alpha == fundo, axis=-1)] = 0

    return image_without_alpha


def increase_contrast_brightness(img):
    alpha = 3  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)

    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


def gamma_correction(img, k):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    invGamma = 1.0 / k
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    result = cv2.LUT(img_gray, table)
    #cv2.imwrite('result4.png', result)
    return result


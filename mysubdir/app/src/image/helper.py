import cv2
import numpy as np
from pytesseract import image_to_data, Output
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

def sort_contours(contours, method="left-to-right"):
    logger.info('[sort_contours] sort contours process')

    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    contours, bounding_boxes = zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][i], reverse=reverse))
    return contours, bounding_boxes


def resize(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    dim = (width, height)
    return cv2.resize(image, dim)


def reject_outliers(data, m=2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(data))

    return data[s < m]


def decide_zoom_factor(image):
    logger.info('[decide_zoom_factor] starting process')
    
    d = image_to_data(image, output_type=Output.DICT, lang='premier-pet')
    h = reject_outliers(np.array(d['height']))
    zoom =  30/(sum(h)/len(h))

    logger.info('[decide_zoom_factor] decided zoom %d' % zoom)
    return zoom

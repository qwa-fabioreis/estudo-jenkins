import cv2
from app.lib.ccvwrapper import ccvwrapper
import numpy as np
import logging


logger = logging.getLogger()

def identify_text_areas(image):
    logger.info('[identify_text_areas] starting process of identifying text areas')

    byte_image = cv2.imencode('.jpg', image)[1].tobytes()
    swt_result_raw = ccvwrapper.swt(byte_image, image.shape[1], image.shape[0])

    swt_result_array = np.asarray(swt_result_raw).astype(int)

    swt_result = np.reshape(swt_result_array, (int(len(swt_result_array) / 4), 4))

    return join_blocks(image, swt_result)


def join_blocks(image, swt_result):
    logger.info('[join_blocks] starting process of identifying blocks')

    blank_image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
    blank_image[:] = (255, 255, 255)

    for x, y, w, h in swt_result:
        blank_image = cv2.rectangle(blank_image, (x - 10, y - int(h / 2)), (x + w + 10, y + 2*h),
                                    (0, 0, 0), -1)


    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blank_image = cv2.erode(blank_image, kernel, iterations=2)
    blank_image = cv2.blur(blank_image, (20, 20))

    contours, _ = cv2.findContours(blank_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        boxes.append((x, y, w, h))
        #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


    return boxes


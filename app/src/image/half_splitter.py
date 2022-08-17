import cv2
import numpy as np
import logging
from ..logger.image_logger import ImageLogger


logger = logging.getLogger()


def split_half(img):
    logger.info('[split_half] starting process of splitting in half')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ImageLogger.log_image('split_half1.png',img)
    kernel_len = np.array(gray).shape[1] // 100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    image_1 = cv2.erode(gray, ver_kernel, iterations=3)
    ImageLogger.log_image('split_half2.png', image_1)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    ImageLogger.log_image('split_half3.png', vertical_lines)
    low_threshold, high_threshold = 10, 150

    edges = cv2.Canny(vertical_lines, low_threshold, high_threshold)
    ImageLogger.log_image('split_half4.png', edges)
    rho = 1
    theta = np.pi / 180
    threshold = 20
    min_line_length = 0.7 * img.shape[0]
    max_line_gap = 1
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    xs = [line[0][0] for line in lines if line[0][0] == line[0][2]]

    halfx = img.shape[1] / 2
    xs.append(halfx)
    xs.sort()
    index = xs.index(halfx)
    xmax = xs[index + 1]
    xmin = xs[index - 1]
    half = int((xmax - xmin) / 2) + xmin

    logger.info('[split_half] xmin = %d, xmax = %d, half = %d ' % (xmin, xmax, half))
    return half

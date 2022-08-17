import numpy as np
import cv2
from ..image.helper import sort_contours
import random
from ..image.half_splitter import split_half
import logging
from ..logger.image_logger import ImageLogger


logger = logging.getLogger()

def binarize_img(img):
    img = img.copy()
    img[np.where((img <= [35, 35, 35]).all(axis=2))] = [255, 255, 255]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    img_bin = 255 - thresh
    return img_bin


def detect_table(img):
    logger.info('[detect_table] starting to detect tables')
    half = split_half(img)
    img_ = img.copy()
    color = img[int(img.shape[0]/2), half]
    #img_com_fill = fill2(img_, color)
    #im_bin_com_fill = binarize_img(img_com_fill)
    im_bin = binarize_img(img_)
    im_bin2 = binarize_img(img)
   
 #   tables = detect_table_(im_bin_com_fill[:, half:], half, img)
 #   tables += detect_table_(im_bin_com_fill[:, :half], 0, img)
    tables = detect_table_(im_bin[:, half:], half, img)
    tables += detect_table_(im_bin[:, :half], 0, img)
    tables += detect_table_(im_bin2[:, half:], half, img)
    tables += detect_table_(im_bin2[:, :half], 0, img)
    tables += detect_table_(im_bin2[:, half:], half, img, 5)
    tables += detect_table_(im_bin2[:, :half], 0, img, 5)

    return tables


def detect_table_(img_bin, offset, img, vertical_dilate_iteractions=3):
    ImageLogger.log_image('table_finder4-%d-%d.png' % (offset, vertical_dilate_iteractions), img_bin)
 
    kernel_len = np.array(img_bin).shape[1] // 100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    ImageLogger.log_image('table_finder5-%d-%d.png' % (offset, vertical_dilate_iteractions), image_1)

    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=vertical_dilate_iteractions)
    ImageLogger.log_image('table_finder6-%d-%d.png' % (offset, vertical_dilate_iteractions), vertical_lines)

    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    ImageLogger.log_image('table_finder7-%d-%d.png' % (offset, vertical_dilate_iteractions), image_2)

    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=5)
    ImageLogger.log_image('table_finder8-%d-%d.png' % (offset, vertical_dilate_iteractions), horizontal_lines)

    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    img_vh = cv2.erode(~img_vh, kernel, iterations=3)
    _, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    ImageLogger.log_image('table_finder9-%d-%d.png' % (offset, vertical_dilate_iteractions), img_vh)

    contours, _ = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom.
    contours, bounding_boxes = sort_contours(contours, method="top-to-bottom")

    heights = [bounding_boxes[i][3] for i in range(len(bounding_boxes))]
    mean = np.mean(heights)

    box = []

    ImageLogger.log_image('table_finder10-%d-%d.png' % (offset, vertical_dilate_iteractions), img_bin)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if 14 <= w < int(img_bin.shape[0] * 0.9) and 10 <= h < int(img_bin.shape[0] * 0.7) \
              and h/w < 8 and w/h < 8:
            box.append([x + offset, y, w, h]) 
        cv2.rectangle(img,(x+offset,y),(x+w+offset,y+h),(random.randint(0,255),255,random.randint(0,255)),3)
    ImageLogger.log_image('table_finder11-%d-%d.png' % (offset, vertical_dilate_iteractions), img)
    row = []
    column = []

    #Sorting the boxes to their respective row and column
    for i in range(len(box)):
        if i == 0:
            column.append(box[i])
            previous = box[i]
        else:
            if box[i][1] <= previous[1] + mean/2 + 40:
                column.append(box[i])
                previous = box[i]
                if i == len(box)-1:
                    row.append(column)
            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    countcol = 0

    for i in range(len(row)):
        countcol = len(row[i])
        if countcol > countcol:
            countcol = countcol

        center = [int(row[i][j][0] + row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center = np.array(center)
        center.sort()

    finalboxes = []
    d_tables = []
    for i in range(len(row)):
        lis = []
        d_table = {}
        for k in range(0, countcol):
            lis.append([])
        if len(row[i]) == 1:
            d_table[row[i][0][1]] = [row[i][0][1]]
        for j in range(1,len(row[i])):
            if row[i][j][1] not in d_table:
                d_table[row[i][j][1]] = [row[i][j]]
            else:
                d_table[row[i][j][1]].append(row[i][j])

            diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        for key in d_table:
            d_table[key].sort()
        d_tables.append(d_table)
        lis = [l for l in lis if len(l) > 1]
        finalboxes.append(lis)

    return d_tables


def fill2(img,color):

    i_, j_, _ = img.shape
    pixels = []
    for j in range(1, j_ - 2):
        for i in range(1, i_ - 2):
            if np.all(img[i][j] == img[i-1][j - 1]) and \
                np.all(img[i][j] == img[i][j - 1]) and \
                np.all(img[i][j] == img[i+1][j-1]) and \
                np.all(img[i][j] == img[i - 1][j]) and \
                np.all(img[i][j] == img[i + 1][j]) and \
                np.all(img[i][j] == img[i - 1][j + 1]) and \
                np.all(img[i][j] == img[i][j + 1]) and \
                np.all(img[i][j] == img[i + 1][j + 1]) and \
                np.all(img[i][j] == img[i + 2][j + 1]) and \
                  np.all(img[i][j] == img[i + 1][j + 2]):

                pixels.append((i,j))
    for i,j in pixels:
        img[i][j] = color
    ImageLogger.log_image('fill.png', img)
    return img

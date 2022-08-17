import numpy as np
import cv2
from ..image.helper import sort_contours


def binarize_img(img):
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    return thresh

def test_threshold_by_background(img):
    background_color = img[-1,-1]
    img[np.where((img == background_color).all(axis=2))] = [255,255,255]
    return img


def detect_table(img):
    img_ = img.copy()
    img_ = test_threshold_by_background(img_)
    im_bin = binarize_img(img_)
    return detect_table_(im_bin)


def detect_table_(img_bin):

    kernel_len = np.array(img_bin).shape[1] // 100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=2)

    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=2)
    image_2 = cv2.erode(img_bin, hor_kernel, iterations=2)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=2)
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    _, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom.
    contours, bounding_boxes = sort_contours(contours, method="top-to-bottom")

    heights = [bounding_boxes[i][3] for i in range(len(bounding_boxes))]
    mean = np.mean(heights)

    box = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if 100 < w < int(img_bin.shape[0] * 0.7) and 15 < h < int(img_bin.shape[0] * 0.7):
            box.append([x, y, w, h])
            cv2.rectangle(img_bin, (x, y), (x+w, y+h), (66, 243, 12), 2)

    row = []
    column = []

    #Sorting the boxes to their respective row and column
    for i in range(len(box)):
        if i == 0:
            column.append(box[i])
            previous = box[i]
        else:

            if box[i][1] <= (previous[1] + mean/2 + 100):
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
            d_table[row[i][0][1]] = [row[i][0]]
        for j in range(0,len(row[i])):
            r = find_range(d_table, row[i][j][1])

            if r is None:
                d_table[row[i][j][1]] = [row[i][j]]
            else:
                row[i][j][1] -= r
                d_table[row[i][j][1]].append(row[i][j])

            diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        for key in d_table:
            d_table[key].sort()
        d_tables.append(d_table)
        lis = [l for l in lis if len(l) > 0]
        finalboxes.append(lis)

    return d_tables


def find_range(d, y):
    if y in d:
        return 0
    if y - 1 in d:
        return 1
    if y - 2 in d:
        return 2
    if y - 3 in d:
        return 3
    if y + 1 in d:
        return -1
    if y + 2 in d:
        return -2
    if y + 3 in d:
        return -3
    return None

def change_colors(img):

    unique, counts = np.unique(img.reshape(-1,3), axis=0, return_counts=True)
    img = img.copy()
    img[np.where((img > unique[np.argmax(counts)]).all(axis=2))] = [255, 255, 255]
    img[np.where((img < unique[np.argmax(counts)]).all(axis=2))] = [0,0,0]
    return img

def fill(img,i):
    i_, j_, _ = img.shape
    for i in range(1, i_ - 1,2):
        for j in range(1, j_ - 1,2):
            if np.all(img[i][j] == img[i-1][j]) and np.all(img[i-1][j] == img[i][j-1]) and np.all(img[i][j-1] == img[i-1][j-1]):
                img[i][j] = img[i-1][j] = img[i][j-1] = img[i-1][j-1] = (120, 120, 120)
    img[np.where((img != [120, 120, 120]).all(axis=2))] = [255, 255, 255]
    return img


def prepare_image(img):
    img_bin = 255 - img
    kernel_len = np.array(img_bin).shape[1] // 100
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    bitxor = cv2.bitwise_xor(img, img_vh)
    bitnot = cv2.bitwise_not(bitxor)

    return img_vh, bitnot, bitxor

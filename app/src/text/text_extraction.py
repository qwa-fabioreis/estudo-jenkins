from pytesseract import image_to_data, image_to_boxes, Output
import cv2
from ..text.utils import remove_white_space, remove_punctuation, remove_punctuation_from_list, remove_white_space_from_list
import numpy as np
from ..logger.image_logger import ImageLogger
import logging


logger = logging.getLogger()
dicionario = 'premier-pet'


def extract_text_from_blocks(img, blocks):
    logger.info('[extract_text_from_blocks] start')
    extracted_texts = []
    for block in blocks:
        extracted_texts.append(extract_text_from_block(img, block))

    return extracted_texts


def extract_text_from_block(img, block):
    x, y, w, h = block

    img_resize = img.copy()
    d = image_to_data(img_resize[y:y+h, x:x+w], output_type=Output.DICT, lang=dicionario)
    
    for i in range(len(d['top'])):
        d['top'][i] += y

    for i in range(len(d['left'])):
        d['left'][i] += x

    if len(d['text']) > 1:
        d = remove_punctuation(d)
        d = remove_white_space(d)
    logger.debug('texto extraido ', d['text'])

    # Alterado o logger para exportar apenas o bloco da (x,y,w,h) da imagem ao inves da imagem inteira como estava sendo feito
    ImageLogger.log_image('im%d_%d_%d_%d.png'%(x,y,w,h), img_resize[y:y+h, x:x+w])
    return d


def extract_boxes_from_blocks(img, blocks):
    extracted_texts = []
    for block in blocks:
        extracted_texts.append(extract_boxes_from_block(img, block))

    return extracted_texts


def extract_boxes_from_block(img, block):
    x, y, w, h = block

    r = image_to_boxes(img[y:y+h, x:x+w])

    boxes = [[abs(b - int(a)) for a, b in zip(word.split(' ')[1:5], [-x, y+h, -x, y+h])] for word in r.split('\n')]

    letter = [word.split(' ')[0] for word in r.split('\n')]
    letter = remove_punctuation_from_list(letter)

    d = {'boxes': boxes, 'letter': letter}
    d = remove_white_space_from_list(d)

    return d


def erase_circles(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.5, minDist=300, param1=70,param2=10,minRadius=5,maxRadius=30)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)

    return img
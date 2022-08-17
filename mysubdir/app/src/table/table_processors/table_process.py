from __future__ import annotations
from pytesseract import image_to_data, Output
from ...text.utils import contains, extract_word_boxes, remove_white_space
import cv2


class TableProcessor:

    @staticmethod
    def compare_table(d_table, image, section):
        pass

    @staticmethod
    def extract_correct_word_boxes(rows, d_text, x, y, begin=0, lower=False, can_remove_white_space=False,
                                                                      should_join=False):
        """
        Compare list of cells with list of extracted words. Example:
        ['aaa','bbb','ccc']
        ['ijjni','aaa','bbb', 'ccc']
        returns the location of the words, if they are a match and
        updates status (found or not)
        :param d_text:
        :param x:
        :param y:
        :return:
        """

        if lower:
            for i in range(len(d_text['text'])):
                d_text['text'][i] = d_text['text'][i].lower()

        word_boxes = []

        for row in rows:
            word = ' '.join([str(cell) for cell in row])
            if lower:
                word = word.lower()
            if can_remove_white_space:
                d_text = remove_white_space(d_text)

            if can_remove_white_space and should_join:
                word = word.replace(' ', '')

            c = contains(word.split(' '), d_text['text'][begin:])

            if c is not False:
                for w in row:
                    w.found = True
                word_boxes += extract_word_boxes(c, d_text, x, y, 5, 5, 1, begin)
                begin += c[1]
        return word_boxes

    @staticmethod
    def extract_correct_word_boxes_list(rows, d_text, x, y, begin=0, lower=False, can_remove_white_space=False,
                                                                                should_join=False):
        """
     Compare list of cells with list of extracted words. Example:
            ['aaa','bbb','ccc']
            ['ijjni','aaa','bbb', 'ccc']
      returns the location of the words, if they are a match and
      updates status (found or not)
      :param d_text:
      :param x:
      :param y:
      :param should_join:
      :return:
        """
        word_boxes = []

        if should_join:
            word = ' '.join([str(cell).replace(' ', '') for cell in rows])
        else:
            word = ' '.join([str(cell) for cell in rows])

        if lower:
            for i in range(len(d_text['text'])):
                d_text['text'][i] = d_text['text'][i].lower()
            word = word.lower()

        if can_remove_white_space:
           d_text = remove_white_space(d_text)

        if can_remove_white_space and should_join:
           word = word.replace(' ', '')

        if len(word) > 0:
           c = contains(word.split(' '), d_text['text'][begin:])
           if c is not False:
              for w in rows:
                  w.found = True

              word_boxes += extract_word_boxes(c, d_text, x, y, 5, 5, 1, begin)

        return word_boxes

    @staticmethod
    def compare_single_text(cell, d_text, x, y, can_remove_white_space=True,
                            line_begin=0, line_end=None):
        """
        Compare single text
        :param d_text:
        :param x:
        :param y:
        :return:
        """
        if line_end is None:
            line_end = len(d_text['text'])

        if can_remove_white_space:
            d_text = remove_white_space(d_text)

        word_boxes = []
        word = cell.text

        c = contains([w for w in word.split(' ') if len(w) > 0 ], d_text['text'][line_begin:line_end])

        if c is not False:
            cell.found = True
            word_boxes += extract_word_boxes(c, d_text, x, y, 5, 5, 1, line_begin)

        return word_boxes

    @staticmethod
    def extract_correct_word_boxes_join_cols(rows, d_text, x, y, lower=True):
        """
        Compare more than one column to extracted text. Example:
        12 | g
        56 | g
        is going to be compared as
        12g
        56g
        :param d_text:
        :param x:
        :param y:
        :return:
        """

        if lower:
            for i in range(len(d_text['text'])):
                d_text['text'][i] = d_text['text'][i].lower()
        begin = 0
        word_boxes = []

        for row in rows:
            word = ''.join([str(r) for r in row])

            c = contains(word.split(' '), d_text['text'][begin:])
            if c is not False:

                for r in row:
                    r.found = True
                word_boxes += extract_word_boxes(c, d_text, x, y, 5, 5, 1, begin)
                begin += c[1]
        return word_boxes

    @staticmethod
    def separate_lines(d_text):
        """
        Separate returned text dictionary in lines. The lines are delimited
         by the index in the dictionary. A value smaller than the previous is
        considered a new line. Example:
        d[left] = [1,3,5, 0, 2, 1, 3, 4]
         1 3  5
        0 2
         1 3 4
        Would return:
        [(0,3),(3,5),(2,4)]
        :return:
        """
        lines = []
        prev_l = 0
        for i, l in enumerate(d_text['left'][1:], 1):
            if l < d_text['left'][i - 1]:
                lines.append((prev_l, i))
                prev_l = i
        lines.append((prev_l, i))
        return lines

    @staticmethod
    def compare_title(coordinate, image, title, config="--psm 4"):
        x, y, w, h = coordinate

        column4_extracted = image_to_data(image[y:y + h, x:w + x], config=config,
                                          output_type=Output.DICT, lang='por+premier-pet')
        word_box = TableProcessor.compare_single_text(title, column4_extracted, x, y)

        if len(word_box) == 0:
            column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                              config='--psm 7',
                                              output_type=Output.DICT,
                                              lang='premier-pet')

            word_box = TableProcessor.compare_single_text(title, column1_extracted, x, y)

        return word_box

    @staticmethod
    def extract_correct_word_boxes_no_order(rows, d_text, x, y, lower=False, remove_white_space=False):
        """
        Compare list of cells with list of extracted words. Example:
        ['aaa','bbb','ccc']
        ['ijjni','aaa','bbb', 'ccc']
        returns the location of the words, if they are a match and
        updates status (found or not)
        :param d_text:
        :param x:
        :param y:
        :return:
        """

        if lower:
            for i in range(len(d_text['text'])):
                d_text['text'][i] = d_text['text'][i].lower()

        word_boxes = []

        for row in rows:
            word = ' '.join([str(cell) for cell in row])
            if lower:
                word = word.lower()
            if remove_white_space:
                word = word.replace(' ', '')

            c = contains(word.split(' '), d_text['text'])
            if c is not False:
                for w in row:
                    w.found = True
                word_boxes += extract_word_boxes(c, d_text, x, y, 5, 5, 1)

        return word_boxes

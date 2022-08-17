from pytesseract import image_to_data, image_to_string, Output
from .table_process import TableProcessor
from ...text.utils import remove_white_space
import cv2


class FullTableProcessor(TableProcessor):
    """
    This is to be used when the whole table is in one box
    """

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())
        x, y, w, h = d_table[y_coordinates[0]][0]
        table_title = image_to_string(image[y:y + h, x:w + x], lang='por+premier-pet').replace(' ', '')

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows

                if len(rows[0][0].text.upper()) > 3 and rows[0][0].text.upper().replace(' ', '') in table_title:
 
                    column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 1',
                                                      output_type=Output.DICT, lang='por+premier-pet')
                    column1_extracted = remove_white_space(column1_extracted)

                    lines = FullTableProcessor.separate_lines(column1_extracted)
                    if 'NÍVEIS DE GARANTIA' in rows[0][0].text.upper():

                        col1 = rows[1:,0:2]
                        col2 = rows[1:,2:4]
                        col3 = rows[1:,4:]
                        for row1, row2, row3, line in zip(col1, col2, col3, lines):

                            word_boxes += FullTableProcessor.extract_correct_word_boxes_list(row1, column1_extracted,
                                                                                            x, y, line[0])

                            word_boxes += FullTableProcessor.extract_correct_word_boxes_list(row2, column1_extracted,
                                                                                            x, y, line[0], False, True, True)

                            word_boxes += FullTableProcessor.extract_correct_word_boxes_list(row3, column1_extracted,
                                                                                            x, y, line[0])

                    else:
                        for row, line in zip(rows[1:], lines):
                            for cell in row:
                                word_boxes += FullTableProcessor.compare_single_text(cell, column1_extracted, x, y,
                                                                       line[0], line[1])

                    break

        return word_boxes

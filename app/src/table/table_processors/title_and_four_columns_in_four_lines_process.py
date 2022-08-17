from pytesseract import image_to_data, image_to_string, Output
import numpy as np
import cv2
from .table_process import TableProcessor


class TitleAndFourColumnsInFourLinesProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        x, y, w, h = d_table[y_coordinates[0]][0]
        table_title = image_to_string(image[y:y + h, x:w + x], lang='por+premier-pet').replace(' ', '')

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                if len(rows[0][0].text) > 1 and rows[0][0].text.replace(' ', '').upper() in table_title.upper():
                    subtitle1 = rows[1][0]
                    subtitle2 = rows[1][1]
                    subtitle3 = rows[1][2]
                    subtitle4 = rows[1][3]
                    rows[0][0].found = True
                    word_boxes += [[x, y, w, h]]

                    word_boxes += TitleAndFourColumnsInFourLinesProcessor.compare_title(d_table[y_coordinates[1]][0], image, subtitle1)

                    word_boxes += TitleAndFourColumnsInFourLinesProcessor.compare_title(d_table[y_coordinates[1]][1], image, subtitle2)

                    word_boxes += TitleAndFourColumnsInFourLinesProcessor.compare_title(d_table[y_coordinates[1]][2], image, subtitle3)

                    word_boxes += TitleAndFourColumnsInFourLinesProcessor.compare_title(d_table[y_coordinates[1]][3], image, subtitle4)

                    porte1 = rows[2][0]
                    porte2 = rows[4][0]
                    porte3 = rows[7][0]

                    # porte
                    portes = (porte1, porte2, porte3)

                    recomendacoes_mini = rows[2:4, 0:]
                    recomendacoes_pequeno = rows[4:7, 0:]
                    recomendacoes_medio = rows[7:, 0:]

                    recomendacoes = (recomendacoes_mini, recomendacoes_pequeno, recomendacoes_medio)

                    for coordinate, recomendacao in zip(y_coordinates[2:], recomendacoes):
 
                        for i, cell in enumerate(d_table[coordinate]):
                            x, y, w, h = cell
                            d_text = image_to_data(image[y:y + h, x:w + x],
                                                   config='-c tessedit_char_whitelist=0123456789kg   --psm 4',
                                                   output_type=Output.DICT,
                                                   lang='premier-pet')
                            word_boxes += TitleAndFourColumnsInFourLinesProcessor.extract_correct_word_boxes_list(
                                recomendacao[:, i], d_text, x, y, 0, True, True, True)

                    for coordinate, porte in zip(y_coordinates[2:], portes):
                        x, y, w, h = d_table[coordinate][0]
                        word_boxes += TitleAndFourColumnsInFourLinesProcessor.compare_title(d_table[coordinate][0], image, porte)

                    break

        return word_boxes

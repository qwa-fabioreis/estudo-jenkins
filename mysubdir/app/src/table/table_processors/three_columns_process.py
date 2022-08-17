from pytesseract import image_to_data, Output
from .table_process import TableProcessor


class ThreeColumnsProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                if rows[0][0].text.upper() == 'NÍVEIS DE GARANTIA':
                    column1 = rows[1:, 0:2]
                    column2 = rows[1:, 2:3]
                    column3 = rows[1:, 3:5]

                    word_boxes += ThreeColumnsProcessor.compare_column(d_table[y_coordinates[0]][0], image, column1)
                    word_boxes += ThreeColumnsProcessor.compare_column(d_table[y_coordinates[0]][1], image, column2)
                    word_boxes += ThreeColumnsProcessor.compare_column(d_table[y_coordinates[0]][2], image, column3)

                    break

        return word_boxes

    @staticmethod
    def compare_column(coordinate, image, column):

        x, y, w, h = coordinate
        column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 4', output_type=Output.DICT,
                                          lang='por+premier-pet')
        return ThreeColumnsProcessor.extract_correct_word_boxes(column, column1_extracted, x, y)

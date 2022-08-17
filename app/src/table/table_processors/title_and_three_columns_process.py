from pytesseract import image_to_data, image_to_string, Output
from .table_process import TableProcessor


class TitleAndThreeColumnsProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        x, y, w, h = d_table[y_coordinates[0]][0]
        table_title = image_to_string(image[y:y + h, x:w + x], lang='por+premier-pet')

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows

                if rows[0][0].text.upper() in table_title.upper():

                    column1 = rows[1:, 0:2]
                    column2 = rows[1:, 2:3]
                    column3 = rows[1:, 3:5]

                    word_boxes += TitleAndThreeColumnsProcessor.compare_column(d_table[y_coordinates[1]][0], image, column1)
                    word_boxes += TitleAndThreeColumnsProcessor.compare_column(d_table[y_coordinates[1]][1], image, column2, 'eng')
                    word_boxes += TitleAndThreeColumnsProcessor.compare_column(d_table[y_coordinates[1]][2], image, column3, 'eng')

                    break

                return word_boxes

    @staticmethod
    def compare_column(coordinate, image, column, lang='por+premier-pet'):

        x, y, w, h = coordinate
        column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 4',
                                          output_type=Output.DICT,
                                          lang=lang)

        return TitleAndThreeColumnsProcessor.extract_correct_word_boxes_list(column, column1_extracted, x, y)

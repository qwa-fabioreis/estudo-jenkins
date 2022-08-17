from pytesseract import image_to_data, image_to_string, Output
from .table_process import TableProcessor


class TitleAndNLinesSameColumnsProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        x, y, w, h = d_table[y_coordinates[0]][0]
        table_title = image_to_string(image[y:y + h, x:w + x], lang='por+premier-pet')

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                if len(rows[0][0].text.upper()) > 1 and rows[0][0].text.upper().replace(' ', '') \
                        in table_title.upper().replace(' ', ''):

                    column1 = rows[1:, 0:1]
                    column2 = rows[1:, 1:3]

                    for column, y_ in zip(column1, y_coordinates[1:]):
                        coordinate = d_table[y_][0]
                        word_boxes += TitleAndNLinesSameColumnsProcessor.compare_column(
                              coordinate, image, column)

                    for column, y_ in zip(column2, y_coordinates[1:]):
                        coordinate = d_table[y_][1]
                        word_boxes += TitleAndNLinesSameColumnsProcessor.compare_column(
                              coordinate, image, column)

                    break
        return word_boxes

    @staticmethod
    def compare_column(coordinate, image, column, config='--psm 7'):
        x, y, w, h = coordinate

        column1_extracted = image_to_data(image[y:y+h, x:x+w],
                                          config=config,
                                          output_type=Output.DICT,
                                          lang='por+premier-pet')
        word_box = TitleAndNLinesSameColumnsProcessor.extract_correct_word_boxes_list(column,column1_extracted, x,
                                                                                               y, 0, False, True, False)

        if len(word_box) == 0:
            column1_extracted = image_to_data(image[y:y + h, x:x + w], config = config, output_type=Output.DICT, lang='premier-pet')

            word_box = TitleAndNLinesSameColumnsProcessor.extract_correct_word_boxes_list(column, column1_extracted,x,
                                                                                                       y, 0, False, True, True)

        return word_box

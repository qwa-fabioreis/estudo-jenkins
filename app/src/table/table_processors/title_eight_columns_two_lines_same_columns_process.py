from pytesseract import image_to_data, Output
from .table_process import TableProcessor


class TitleEightColumnsAndTwoLinesSameColumnsProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):
        y_coordinates = list(d_table.keys())

        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows

                if len(rows[0]) > 1 and len(rows[0][1].text) > 1 and rows[0][1].text.upper().replace(' ', '') in '1ºDIA':
                    x, y, w, h = d_table[y_coordinates[0]][0]
                    days = image_to_data(image[y:y + h, x:w + x], config='--psm 7', output_type=Output.DICT, lang='premier-pet')
                    days_doc = rows[0, 1:8]

                    word_boxes += TitleEightColumnsAndTwoLinesSameColumnsProcessor.extract_correct_word_boxes(days_doc, days, x, y)

                    # second column

                    for i, y_ in enumerate(y_coordinates[1:], 1):
                        for row, coordinate in zip(rows[i], d_table[y_]):
                            word_boxes += TitleEightColumnsAndTwoLinesSameColumnsProcessor.compare_title(coordinate, image, row)

                    break

        return word_boxes


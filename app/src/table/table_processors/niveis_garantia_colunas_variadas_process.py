from pytesseract import image_to_data, image_to_string, Output
from .table_process import TableProcessor


class NiveisGarantiaColunasVariadasProcessor(TableProcessor):

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
                    for table_row, y_coordinate in zip(rows[1:], y_coordinates[1:]):
                        for cell, coordinate in zip([cell for cell in table_row if len(cell.text) > 1],
                                                    d_table[y_coordinate]):
                            x, y, w, h = coordinate

                            column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 7',
                                                              output_type=Output.DICT, lang='por+premier-pet')
                            word_boxes += NiveisGarantiaColunasVariadasProcessor.compare_single_text(cell,
                                                                                                     column1_extracted,
                                                                                                     x, y, True)
                    break

        return word_boxes

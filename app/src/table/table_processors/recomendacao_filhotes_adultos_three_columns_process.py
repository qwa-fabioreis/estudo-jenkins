from pytesseract import image_to_data, Output
from .table_process import TableProcessor


class RecomendacaoFilhotesAdultosThreeColumnsProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):
        y_coordinates = list(d_table.keys())

        fulltable = []
        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                # nesse caso sao duas tabelas
                if len(rows[0][0].text.upper()) > 3 and rows[0][0].text.upper().strip(
                        ' ') in 'RECOMENDAÇÃO DIÁRIA DE CONSUMO*':

                    if 'FILHOTES' in rows[1][0].text.upper():
                        fulltable.insert(0, table)
                    else:
                        fulltable.insert(1, table)

        if len(fulltable) == 2:
            table_filhotes = fulltable[0]
            table_adultos = fulltable[1]

            titulo_filhotes = table_filhotes.rows[1][0]
            titulo_tipo_pesos_filhotes = table_filhotes.rows[2:]

            titulo_tipo_pesos_adulto = table_adultos.rows[2:]

            x, y, w, h = d_table[y_coordinates[1]][0]
            column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 7', output_type=Output.DICT,
                                              lang='por+premier-pet')
            word_box = RecomendacaoFilhotesAdultosThreeColumnsProcessor.compare_single_text(titulo_filhotes, column1_extracted, x, y)
            word_boxes += word_box

            word_boxes += RecomendacaoFilhotesAdultosThreeColumnsProcessor.compare_lines(y_coordinates[2:5], titulo_tipo_pesos_filhotes, d_table, image)

            word_boxes += RecomendacaoFilhotesAdultosThreeColumnsProcessor.compare_lines(y_coordinates[6:], titulo_tipo_pesos_adulto, d_table, image)

        return word_boxes

    @staticmethod
    def compare_lines(y_coordinates, texts, d_table, image):
        word_boxes = []
        for coordinates, line in zip(y_coordinates[6:], texts):
            for coordinate, text in zip(d_table[coordinates], line):
                x, y, w, h = coordinate
                column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 7', output_type=Output.DICT,
                                                  lang='por+premier-pet')
                word_box = RecomendacaoFilhotesAdultosThreeColumnsProcessor.compare_single_text(text, column1_extracted, x, y)
                word_boxes += word_box

        return word_boxes

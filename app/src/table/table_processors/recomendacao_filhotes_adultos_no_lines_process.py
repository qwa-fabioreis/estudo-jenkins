from pytesseract import image_to_data, Output
from .table_process import TableProcessor
import logging


logger = logging.getLogger()

class RecomendacaoFilhotesAdultosNoLinesProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):
        y_coordinates = list(d_table.keys())
        logger.info('RecomendacaoFilhotesAdultosNoLinesProcessor')
        fulltable = []
        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                # nesse caso sao duas tabelas
                if 'RECOMENDAÇÃO DIÁRIA DE CONSUMO*' in rows[0][0].text.upper().strip(' ')\
                        or 'ADULTOS' in rows[0][0].text.upper().strip(' '):

                    if 'FILHOTES' in rows[1][0].text.upper():
                        fulltable.insert(0, table)
                    else:
                        fulltable.insert(1, table)

        if len(fulltable) == 2:
            table_filhotes = fulltable[0]
            table_adultos = fulltable[1]

            titulo_tipo_pesos_filhotes = table_filhotes.rows[1:]

            titulo_tipo_pesos_adulto = table_adultos.rows

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[1]][0], image, titulo_tipo_pesos_filhotes[0][0])

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[2]][0], image, titulo_tipo_pesos_filhotes[1][0])
            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[2]][1], image, titulo_tipo_pesos_filhotes[1][1])
            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[2]][2], image, titulo_tipo_pesos_filhotes[1][2])

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_columns(d_table[y_coordinates[3]],
                                                                                      image, titulo_tipo_pesos_filhotes)

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[4]][0], image, titulo_tipo_pesos_adulto[0][0])
            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[5]][0], image, titulo_tipo_pesos_adulto[1][0])
            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[5]][1], image, titulo_tipo_pesos_adulto[1][1])
            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_title(d_table[y_coordinates[5]][2], image, titulo_tipo_pesos_adulto[1][2])

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.compare_columns(d_table[y_coordinates[6]], image, titulo_tipo_pesos_adulto[1:])

        return word_boxes


    @staticmethod
    def compare_columns(coordinates, image, table):
        word_boxes = []

        for coordinate, i in zip(coordinates, range(3)):
            col1 = table[1:, i:i+1]
            x, y, w, h = coordinate
            column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 4',
                                              output_type=Output.DICT, lang='premier-pet')

            word_boxes += RecomendacaoFilhotesAdultosNoLinesProcessor.extract_correct_word_boxes(
                col1, column1_extracted, x, y)
        return word_boxes

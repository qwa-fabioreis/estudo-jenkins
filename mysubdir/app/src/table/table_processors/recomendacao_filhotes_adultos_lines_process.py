from pytesseract import image_to_data, Output
from .table_process import TableProcessor


class RecomendacaoFilhotesAdultosLinesProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):
        y_coordinates = list(d_table.keys())

        fulltable = []
        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows
                # nesse caso sao duas tabelas
                if 'RECOMENDAÇÃO DIÁRIA DE CONSUMO*' in rows[0][0].text.upper().strip(' '):

                    if 'FILHOTES' in rows[1][0].text.upper():
                        fulltable.insert(0, table)
                    else:
                        fulltable.insert(1, table)

        if len(fulltable) == 2:
            table_filhotes = fulltable[0]
            table_adultos = fulltable[1]

            titulo_filhotes = table_filhotes.rows[1][0]
            titulo_tipo_pesos_filhotes = table_filhotes.rows[1:]

            titulo_tipo_pesos_adulto = table_adultos.rows[1:]

            word_boxes += RecomendacaoFilhotesAdultosLinesProcessor.compare_title(d_table[y_coordinates[2]][0], image, titulo_tipo_pesos_filhotes[0][0])

            word_boxes += RecomendacaoFilhotesAdultosLinesProcessor.compare_title(d_table[y_coordinates[1]][0], image, titulo_filhotes)

            word_boxes += RecomendacaoFilhotesAdultosLinesProcessor.compare_lines(y_coordinates[3:5], titulo_tipo_pesos_filhotes[1:], d_table, image)

            word_boxes += RecomendacaoFilhotesAdultosLinesProcessor.compare_title(d_table[y_coordinates[6]][0], image, titulo_tipo_pesos_adulto[0][0])

            word_boxes += RecomendacaoFilhotesAdultosLinesProcessor.compare_lines(y_coordinates[7:], titulo_tipo_pesos_adulto[1:], d_table, image)

        return word_boxes

    @staticmethod
    def compare_lines(y_coordinates, lines, d_table, image):
        word_boxes = []
        for coordinates, line in zip(y_coordinates, lines):
            coordinate0 = d_table[coordinates][0]
            x, y, w, h = coordinate0
            column0_extracted = image_to_data(image[y:y + h, x:w + x],
                                              config='--psm 7',
                                              output_type=Output.DICT,
                                              lang='premier-pet')
            text = line[0]

            word_box = RecomendacaoFilhotesAdultosLinesProcessor.compare_single_text(text, column0_extracted, x, y)
            word_boxes += word_box

            coordinate1 = d_table[coordinates][1]
            x, y, w, h = coordinate1
            column1_extracted = image_to_data(image[y:y + h, x:w + x],
                                              config='-c tessedit_char_whitelist=0123456789kg,.- --psm 7',
                                              output_type=Output.DICT,
                                              lang='premier-pet')

            word_box = RecomendacaoFilhotesAdultosLinesProcessor.extract_correct_word_boxes_list(line[1:], column1_extracted, x, y, 0, False, True, True)
            word_boxes += word_box

        return word_boxes

from pytesseract import image_to_data, Output
import cv2
from .table_process import TableProcessor
from ...image.helper import resize


class RecomendacaoPesoIdadeFiveColProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        # 1 linha/coluna : tabela inteira
        # 2 peso esperado/ idade
        # 3 faixa de meses
        # 4 tamanho/peso
        word_boxes = []
        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows

                if len(rows[0][0].text.upper()) > 3 and rows[0][0].text.upper() in 'RECOMENDAÇÃO DIÁRIA DE CONSUMO*':

                    peso_esperado = rows[1][0]
                    idade = rows[1][1]
                    # titulos da tabela
                    titulos_da_tabela = (peso_esperado, idade)

                    intervalo1 = rows[2][2]

                    intervalo2 = rows[2][4]
                    intervalo3 = rows[2][6]
                    intervalo4 = rows[2][8]

                    # intervalos
                    intervalos = (intervalo1, intervalo2, intervalo3, intervalo4)

                    pesos = rows[3:, 0:1]

                    recomendacoes_idade1 = rows[3:, 1:3]
                    recomendacoes_idade2 = rows[3:, 3:5]
                    recomendacoes_idade3 = rows[3:, 5:7]
                    recomendacoes_idade4 = rows[3:, 7:8]

                    recomendacoes = (recomendacoes_idade1, recomendacoes_idade2, recomendacoes_idade3,
                                     recomendacoes_idade4)

                    word_boxes += RecomendacaoPesoIdadeFiveColProcessor.compare_lines(d_table, y_coordinates[1], titulos_da_tabela, image, '--psm 4')

                    word_boxes += RecomendacaoPesoIdadeFiveColProcessor.compare_lines(d_table, y_coordinates[2], intervalos, image, '-c '
                                                                                                   'tessedit_char_whitelist=0123456789ae --psm 4')

                    coordinate = y_coordinates[3]

                    word_boxes += RecomendacaoPesoIdadeFiveColProcessor.compare_columns(d_table, coordinate, image, recomendacoes)

                    word_boxes += RecomendacaoPesoIdadeFiveColProcessor.compare_column(d_table, coordinate, image, pesos)

                    break

        return word_boxes

    @staticmethod
    def compare_lines(d_table, y_coordinates, texts, image, config):
        word_boxes = []
        for coordinates, text in zip(d_table[y_coordinates], texts):
            x, y, w, h = coordinates
            column1_extracted = image_to_data(image[y:y + h, x:w + x],
                                              config=config,
                                              output_type=Output.DICT,
                                              lang='premier-pet')
            word_box = RecomendacaoPesoIdadeFiveColProcessor.compare_single_text(str(text), column1_extracted, x, y)

            if len(word_box) == 0:
                column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                  config=config,
                                                  output_type=Output.DICT,
                                                  lang='premier-pet')

                word_box = RecomendacaoPesoIdadeFiveColProcessor.compare_single_text(str(text), column1_extracted, x, y)

            word_boxes += word_box

        return word_boxes

    @staticmethod
    def compare_column(d_table, coordinate, image, columns):
        x, y, w, h = d_table[coordinate][0]
        column1_extracted = image_to_data(image[y:y + h, x:w + x],
                                          config='-c tessedit_char_whitelist=,0123456789kg --psm 4',
                                          output_type=Output.DICT,
                                          lang='premier-pet')
        return RecomendacaoPesoIdadeFiveColProcessor.extract_correct_word_boxes_join_cols(columns, column1_extracted, x, y)

    @staticmethod
    def compare_columns(d_table, coordinate, image, columns):
        word_boxes = []
        for i, cell in enumerate(d_table[coordinate][1:]):
            column = columns[i]
            x, y, w, h = cell
            d_text = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                   config='-c tessedit_char_whitelist=0123456789kg   --psm 4',
                                   output_type=Output.DICT,
                                   lang='premier-pet')

            word_boxes += RecomendacaoPesoIdadeFiveColProcessor.extract_correct_word_boxes_join_cols(column, d_text, x, y)

        return word_boxes

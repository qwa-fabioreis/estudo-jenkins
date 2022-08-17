from pytesseract import image_to_data, Output
import cv2
from .table_process import TableProcessor


class RecomendacaoTamanhoIdadeProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

        y_coordinates = list(d_table.keys())

        # 1 linha/coluna : tabela inteira
        # 2 porte/ peso esperado/ idade
        # 3 faixa de meses
        # 4 tamanho/peso
        # 5 tamanho/peso
        # 6 tamanho/peso

        for doc_row in section.rows:
            for table in doc_row.tables:
                rows = table.rows

                if len(rows[0][0].text.upper()) > 3 and rows[0][0].text.upper() in 'RECOMENDAÇÃO DIÁRIA DE CONSUMO*':

                    porte = rows[1][0]
                    peso_esperado = rows[1][1]
                    idade = rows[1][2]
                    # titulos da tabela
                    titulos_da_tabela = (porte, peso_esperado, idade)

                    intervalo1 = rows[2][2]
                    intervalo2 = rows[2][3]
                    intervalo3 = rows[2][4]
                    intervalo4 = rows[2][5]
                    intervalo5 = rows[2][6]

                    # intervalos
                    intervalos = (intervalo1, intervalo2, intervalo3, intervalo4, intervalo5)

                    porte1 = rows[3][0]
                    porte2 = rows[5][0]
                    porte3 = rows[8][0]

                    # porte
                    portes = (porte1, porte2, porte3)

                    recomendacoes_mini = rows[3:5, 0:]
                    recomendacoes_pequeno = rows[5:7, 0:]
                    recomendacoes_medio = rows[7:, 0:]

                    recomendacoes = (recomendacoes_mini, recomendacoes_pequeno, recomendacoes_medio)

                    word_boxes = []

                    # titulos da tabela
                    word_boxes += RecomendacaoTamanhoIdadeProcessor.compare_sigle_column(y_coordinates[1], titulos_da_tabela, d_table, image)

                    word_boxes += RecomendacaoTamanhoIdadeProcessor.compare_sigle_column(y_coordinates[2], intervalos, d_table, image)



                    for coordinate, recomendacao in zip(y_coordinates[3:], recomendacoes):
                        # print(coordinate)
                        for i, cell in enumerate(d_table[coordinate]):
                            x, y, w, h = cell
                            d_text = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                   config='-c tessedit_char_whitelist=0123456789kg   --psm 4',
                                                   output_type=Output.DICT,
                                                   lang='premier-pet')

                            word_boxes += RecomendacaoTamanhoIdadeProcessor.extract_correct_word_boxes(recomendacao[:, i], d_text, x, y, False, True)

                    for coordinate, porte in zip(y_coordinates[3:], portes):
                        x, y, w, h = d_table[coordinate][0]
                        column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 12',
                                                          output_type=Output.DICT, lang='por+premier-pet')
                        word_box = RecomendacaoTamanhoIdadeProcessor.compare_single_text(porte, column1_extracted, x, y)
                        if len(word_box) == 0:
                            column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                              config='--psm 12',
                                                              output_type=Output.DICT, lang='por+premier-pet')
                            word_box = RecomendacaoTamanhoIdadeProcessor.compare_single_text(porte, column1_extracted, x, y)
                        word_boxes += word_box

                    break

        return word_boxes

    @staticmethod
    def compare_sigle_column(y_coordinate, texts, d_table, image):
        word_boxes = []

        for coordinates, text in zip(d_table[y_coordinate], texts):
            x, y, w, h = coordinates
            column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 12',
                                              output_type=Output.DICT, lang='por+premier-pet')
            word_box = RecomendacaoTamanhoIdadeProcessor.compare_single_text(text, column1_extracted, x, y)
            if len(word_box) == 0:
                column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                  config='--psm 12',
                                                  output_type=Output.DICT, lang='por+premier-pet')
                word_box = RecomendacaoTamanhoIdadeProcessor.compare_single_text(text, column1_extracted, x, y)
            word_boxes += word_box

        return word_boxes

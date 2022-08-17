from pytesseract import image_to_data, Output
import cv2
from .table_process import TableProcessor


class RecomendacaoPesoIdadeSixColProcessor(TableProcessor):

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
                    rows[0][0].found = True

                    peso_esperado = rows[1][1]
                    idade = rows[1][2]
                    # titulos da tabela
                    titulos_da_tabela = (peso_esperado, idade)

                    intervalo1 = rows[2][2]

                    intervalo2 = rows[2][3]
                    intervalo3 = rows[2][4]
                    intervalo4 = rows[2][5]
                    intervalo5 = rows[2][6]

                    # intervalos
                    intervalos = (intervalo1, intervalo2, intervalo3, intervalo4, intervalo5)

                    pesos1 = rows[3:5, 1:2]
                    pesos2 = rows[5:8, 1:2]
                    pesos3 = rows[8:12, 1:2]
                    pesos = [pesos1, pesos2, pesos3]

                    porte1 = rows[3:4, 0:1]
                    porte2 = rows[5:7, 0:1]
                    porte3 = rows[8:9, 0:1]
                    portes = [porte1, porte2, porte3]

                    recomendacoes_idade1 = rows[3:5, 2:]
                    recomendacoes_idade2 = rows[5:8, 2:]
                    recomendacoes_idade3 = rows[8:, 2:]

                    recomendacoes = (recomendacoes_idade1, recomendacoes_idade2, recomendacoes_idade3)

                    word_boxes += [d_table[y_coordinates[0]][0]]
                    # titulos da tabela
                    word_boxes += RecomendacaoPesoIdadeSixColProcessor.compare_titles(titulos_da_tabela, d_table,
                                                                                      y_coordinates[1],
                                                                                      image, '--psm 4')

                    word_boxes += RecomendacaoPesoIdadeSixColProcessor.compare_titles(intervalos, d_table,
                                                                                      y_coordinates[2],
                                                                                      image,
                                                                                      '-c tessedit_char_whitelist=0123456789ae')

                    for recomendacao, coordinate in zip(recomendacoes, y_coordinates[3:]):

                        for i, cell in enumerate(d_table[coordinate][1:]):
                            cell_text = recomendacao[:, i:i+1]
                            x, y, w, h = cell
                            d_text = image_to_data(image[y:y + h, x:w + x],
                                                   output_type=Output.DICT,
                                                   lang='premier-pet')

                            word_boxes += RecomendacaoPesoIdadeSixColProcessor.extract_correct_word_boxes(
                                cell_text, d_text, x, y, 0, True, True)

                    # peso
                    for i, coordinate in enumerate(y_coordinates[3:]):
                        x, y, w, h = d_table[coordinate][0]
                        column1_extracted = image_to_data(image[y:y + h, x:w + x], config='--psm 4',
                                                          output_type=Output.DICT, lang='premier-pet')

                        word_box = RecomendacaoPesoIdadeSixColProcessor.extract_correct_word_boxes_no_order(pesos[i],
                                                                                                             column1_extracted,
                                                                                                             x, y, True, True)

                        word_boxes += word_box
                        word_box = RecomendacaoPesoIdadeSixColProcessor.extract_correct_word_boxes(portes[i],
                                                                                                   column1_extracted,
                                                                                                   x, y, 0, True, True)

                        word_boxes += word_box

                    break

        return word_boxes

    @staticmethod
    def compare_titles(titles, d_table, y_coordinate, image, config):
        word_boxes = []
        for coordinates, title in zip(d_table[y_coordinate], titles):

            x, y, w, h = coordinates

            column1_extracted = image_to_data(image[y:y + h, x:w + x], config=config,
                                              output_type=Output.DICT, lang='por+premier-pet')
            word_box = RecomendacaoPesoIdadeSixColProcessor.compare_single_text(title, column1_extracted, x, y)

            if len(word_box) == 0:
                column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                  config='--psm 7',
                                                  output_type=Output.DICT,
                                                  lang='premier-pet')

                word_box = RecomendacaoPesoIdadeSixColProcessor.compare_single_text(title, column1_extracted, x, y)

            word_boxes += word_box

        return word_boxes

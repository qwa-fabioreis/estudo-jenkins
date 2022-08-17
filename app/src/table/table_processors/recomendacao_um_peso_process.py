from pytesseract import image_to_data, Output
import cv2
from .table_process import TableProcessor


class RecomendacaoUmPesoProcessor(TableProcessor):

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

                    raca = rows[2][0]
                    idade = rows[1][0]

                    intervalo_idade = rows[2,1:]

                    recomendacoes_gramas = rows[3, 1:]

                    word_boxes += RecomendacaoUmPesoProcessor.compare_cell(d_table[y_coordinates[1]][0],
                                                                            image, raca)

                    word_boxes += RecomendacaoUmPesoProcessor.compare_cell(d_table[y_coordinates[1]][1],
                                                                           image, idade)

                    word_boxes += RecomendacaoUmPesoProcessor.compare_columns(d_table, y_coordinates[2],
                                                                              image, intervalo_idade)

                    word_boxes += RecomendacaoUmPesoProcessor.compare_columns(d_table, y_coordinates[3],
                                                                             image, recomendacoes_gramas)

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
            word_box = RecomendacaoUmPesoProcessor.compare_single_text(str(text), column1_extracted, x, y)

            if len(word_box) == 0:
                column1_extracted = image_to_data(cv2.bitwise_not(image[y:y + h, x:w + x]),
                                                  config=config,
                                                  output_type=Output.DICT,
                                                  lang='premier-pet')

                word_box = RecomendacaoUmPesoProcessor.compare_single_text(str(text), column1_extracted, x, y)

            word_boxes += word_box

        return word_boxes

    @staticmethod
    def compare_column(d_table, coordinate, image, columns):
        x, y, w, h = d_table[coordinate][0]
        column1_extracted = image_to_data(image[y:y + h, x:w + x],
                                          config='--psm 4',
                                          output_type=Output.DICT,
                                          lang='premier-pet')

        return RecomendacaoUmPesoProcessor.extract_correct_word_boxes_join_cols(columns, column1_extracted, x, y)

    @staticmethod
    def compare_cell(coordinate, image, cell):
        x, y, w, h = coordinate
        column1_extracted = image_to_data(image[y:y + h, x:w + x],
                                          config='--psm 4',
                                          output_type=Output.DICT,
                                          lang='premier-pet')

        return RecomendacaoUmPesoProcessor.compare_single_text(cell, column1_extracted, x, y)


    @staticmethod
    def compare_columns(d_table, coordinate, image, columns):
  
        word_boxes = []
        for i, cell in enumerate(d_table[coordinate]):
            column = columns[i]
            x, y, w, h = cell
            d_text = image_to_data(image[y:y + h, x:w + x],
                                   config='--psm 7',
                                   output_type=Output.DICT,
                                   lang='premier-pet')

            word_boxes += RecomendacaoUmPesoProcessor.compare_single_text(column, d_text, x, y)

        return word_boxes

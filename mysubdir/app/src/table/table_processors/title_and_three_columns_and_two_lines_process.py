from pytesseract import image_to_data, image_to_string, Output
from .table_process import TableProcessor


class TitleAndThreeColumnsAndTwoLinesProcessor(TableProcessor):

    @staticmethod
    def compare_table(d_table, image, section):

            y_coordinates = list(d_table.keys())

            x, y, w, h = d_table[y_coordinates[0]][0]
            table_title = image_to_string(image[y:y+h,x:w+x], lang='por+premier-pet')

            word_boxes = []
            for doc_row in section.rows:
                for table in doc_row.tables:
                    rows = table.rows

                    if len(rows[0][0].text) > 2 and rows[0][0].text.upper() in table_title.upper():

                        subtitle1 = rows[1][0]
                        subtitle2 = rows[1][1]
                        subtitle3 = rows[1][2]
                        rows[0][0].found = True
                        word_boxes += [[x, y, w, h]]
                        x, y, w, h = d_table[y_coordinates[1]][0]

                        column1_extracted = image_to_data(image[y:y+h, x:w+x], config='--psm 4', output_type=Output.DICT, lang='por+premier-pet')
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column1,
                                                                                                          column1_extracted,
                                                                                                          x, y, 0,
                                                                                                          False, True,
                                                                                                          True)

                        x, y, w, h = d_table[y_coordinates[1]][1]
                        column2_extracted = image_to_data(image[y:y+h, x:w+x], config='--psm 4', output_type=Output.DICT, lang='premier-pet')
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column2, column2_extracted, x, y, 0, False, True, True)

                        x, y, w, h = d_table[y_coordinates[1]][2]
                        column3_extracted = image_to_data(image[y:y+h, x:w+x], config='--psm 4', output_type=Output.DICT, lang='premier-pet')
                        
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column3, column3_extracted, x, y, 0, False, True, True)
                        column1 = rows[2:, 0:1]
                        column2 = rows[2:, 1:2]
                        column3 = rows[2:, 2:3]

                        x, y, w, h = d_table[y_coordinates[2]][0]

                        column1_extracted = image_to_data(image[y:y+h, x:w+x], config='-c tessedit_char_whitelist=0123456789kmg --psm 4', output_type=Output.DICT, lang='premier-pet')
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column1, column1_extracted, x, y)

                        x, y, w, h = d_table[y_coordinates[2]][1]
                        column2_extracted = image_to_data(image[y:y+h, x:w+x], config='-c tessedit_char_whitelist=0123456789kmg --psm 4', output_type=Output.DICT, lang='premier-pet')
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column2, column2_extracted, x, y)
                        x, y, w, h = d_table[y_coordinates[2]][2]

                        column3_extracted = image_to_data(image[y:y+h, x:w+x], config='-c tessedit_char_whitelist=0123456789kmg --psm 4', output_type=Output.DICT, lang='premier-pet')
                        word_boxes += TitleAndThreeColumnsAndTwoLinesProcessor.extract_correct_word_boxes(column3, column3_extracted, x, y)

                        break

            return word_boxes


from ..text.utils import contains

from .table_processors.table_processor_creator import TableProcessorCreator
from .table_type_chooser import choose_table_type
import logging


logger = logging.getLogger()


def compare_tables(tables, section, image, blocks):
    logger.info('[compare_tables] starting to compare tables')

    result = []

    for table in tables:
        result += compare_table_by_type(table, image, choose_table_type(table), section)


    #return compare_table_to_blocks(section, blocks)
    return result


def compare_table_to_blocks(section, blocks):

    x_offset, y_offset = 5,5
    word_boxes = []
    for doc_row in section.rows:
        for table in doc_row.tables:
            for row in table.rows:

                content = list(
                    [r.text.replace('º', '°').replace(' ', '').replace(',', '').replace('.', '').replace('\n', '').replace(';',
                                                                                                              '').upper()
                     for r in row])
                for block in blocks:
                    c = contains(content, block['letter'])
                    if row.found is False and c is not False:

                        row.found = True
                        for word_index in range(c[0], c[1]):
                            (x, y, w, h) = (
                                int(block['boxes'][word_index][0]), int(block['boxes'][word_index][3]),
                                int(block['boxes'][word_index][2]) - int(block['boxes'][word_index][0]) + x_offset,
                                int(block['boxes'][word_index][1]) - int(block['boxes'][word_index][3]) + y_offset)
                            word_boxes.append((x, y, w, h))
                        break

    return word_boxes


def compare_table_by_type(d_table, image, table_type, section):
    logger.info('[compare_table_by_type] %s' % table_type)
    results = []

    creator = TableProcessorCreator.create(table_type)

    if creator is not None:
        results = creator.compare_table(d_table, image, section)

    return results


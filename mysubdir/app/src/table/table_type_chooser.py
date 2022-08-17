from ..enums.tables_enum import TableType
import logging

logger = logging.getLogger()

def choose_table_type(d_table):
    logger.info('choose table type')
    logger.debug(d_table)

    tab_type = 'undefined'
    y_coordinates = list(d_table.keys())
    # print(y_coordinates)
    # tem duas linhas, primeira soh tem uma coluna, segunda tem tres - comparar segunda linha como coluna
    if len(d_table) == 2 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 3:
        tab_type = TableType.TITLE_AND_THREE_COLUMNS

    elif len(d_table) == 7 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 1 \
        and len(d_table[y_coordinates[2]]) == 3 and len(d_table[y_coordinates[3]]) == 3 \
        and len(d_table[y_coordinates[4]]) == 1 and len(d_table[y_coordinates[5]]) == 3 \
        and len(d_table[y_coordinates[6]]) == 3:
        tab_type = TableType.RECOMENDACAO_FILHOTES_ADULTOS_NO_LINES

    # tem titulo, tres colunas, duas linhas
    elif len(d_table) == 3 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 3 \
            and len(d_table[y_coordinates[2]]) == 3:
        tab_type = TableType.TITLE_AND_THREE_COLUMNS_TWO_LINES

    elif len(d_table) == 5 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 4 and \
            len(d_table[y_coordinates[2]]) == 4 and len(d_table[y_coordinates[3]]) == 4 and len(
        d_table[y_coordinates[4]]) == 4:
        tab_type = TableType.TITLE_FOUR_COLUMNS_IN_FOUR_LINES

    elif len(d_table) == 3 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 8 and \
            len(d_table[y_coordinates[2]]) == 8:
        tab_type = TableType.TITLE_EIGHT_COLUMNS_TWO_LINES

    # tem n linhas, a primeira com apenas uma coluna, as seguintes com varias, porem com a mesma quantidade
    elif len(d_table) > 2 and len(d_table[y_coordinates[0]]) == 1 and verify_if_same_length(d_table, y_coordinates[1:]):
        tab_type = TableType.TITLE_N_LINES_SAME_COLUMNS

    # possui apenas uma linha uma coluna
    elif len(d_table) == 1 and len(d_table[y_coordinates[0]]) == 1 and \
            type(d_table[y_coordinates[0]][0]) is list and len(d_table[y_coordinates[0]][0]) == 4:
        tab_type = TableType.FULL_TABLE

    # possui apenas as 3  colunas, para os casos em q nao encontra o titulo da tabela de niveis de garantia
    elif len(d_table) == 1 and len(d_table[y_coordinates[0]]) == 3:
        tab_type = TableType.THREE_COLUMNS

    elif len(d_table) == 6 and len(d_table[y_coordinates[1]]) == 3 and len(d_table[y_coordinates[2]]) == 5 and \
            len(d_table[y_coordinates[3]]) == 7 and len(d_table[y_coordinates[4]]) == 7 and len(
        d_table[y_coordinates[5]]) == 7:
        tab_type = TableType.RECOMENDACAO_TAMANHO_IDADE

    elif len(d_table) == 4 and len(d_table[y_coordinates[1]]) == 2 and len(d_table[y_coordinates[2]]) == 4 and \
            len(d_table[y_coordinates[3]]) == 5:
        tab_type = TableType.RECOMENDACAO_PESO_IDADE_FIVE_COL

    elif len(d_table) == 6 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 2 and \
            len(d_table[y_coordinates[2]]) == 5 and len(d_table[y_coordinates[3]]) == 6:
        tab_type = TableType.RECOMENDACAO_PESO_IDADE_SIX_COL

    elif len(d_table) > 10 and len(d_table[y_coordinates[0]]) == 1 and \
            len(d_table[y_coordinates[1]]) == len(d_table[y_coordinates[2]]) == 5 and \
            len(d_table[y_coordinates[-1]]) <= 3 and len(d_table[y_coordinates[-2]]) <= 3:
        tab_type = TableType.NIVEIS_GARANTIA_COLUNAS_VARIADAS

    elif len(d_table) > 10 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 1 and \
            len(d_table[y_coordinates[2]]) == len(d_table[y_coordinates[3]]) == len(d_table[y_coordinates[4]]) == 3 and \
            len(d_table[y_coordinates[5]]) == 1:
        tab_type = TableType.RECOMENDACAO_FILHOTES_ADULTOS_THREE_COLUMNS

    elif len(d_table) > 10 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 1 and \
            len(d_table[y_coordinates[2]]) == len(d_table[y_coordinates[3]]) == len(d_table[y_coordinates[4]]) == 2 and \
            len(d_table[y_coordinates[5]]) == 1:
        tab_type = TableType.RECOMENDACAO_FILHOTES_ADULTOS_LINES

    elif len(d_table) == 4 and len(d_table[y_coordinates[0]]) == 1 and len(d_table[y_coordinates[1]]) == 2 and \
                 len(d_table[y_coordinates[2]]) == len(d_table[y_coordinates[3]]) == 5:
        tab_type = TableType.RECOMENDACAO_UM_PESO


    logger.info('RETURNING TABLE TYPE %s' % tab_type)
    return tab_type


def verify_if_same_length(d_table, keys):
    return len(set([len(d_table[key]) for key in keys])) == 1

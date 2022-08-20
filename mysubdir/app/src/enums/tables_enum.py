from enum import Enum

class TableType(Enum):
    FULL_TABLE = 'FULL_TABLE'
    NIVEIS_GARANTIA_COLUNAS_VARIADAS = 'NIVEIS_GARANTIA_COLUNAS_VARIADAS'
    RECOMENDACAO_PESO_IDADE_FIVE_COL = 'RECOMENDACAO_PESO_IDADE_FIVE_COL'
    RECOMENDACAO_PESO_IDADE_SIX_COL = 'RECOMENDACAO_PESO_IDADE_SIX_COL'
    RECOMENDACAO_TAMANHO_IDADE = 'RECOMENDACAO_TAMANHO_IDADE'
    THREE_COLUMNS = 'THREE_COLUMNS'
    TITLE_FOUR_COLUMNS_IN_FOUR_LINES = 'TITLE_FOUR_COLUMNS_IN_FOUR_LINES'
    TITLE_N_LINES_SAME_COLUMNS = 'TITLE_N_LINES_SAME_COLUMNS'
    TITLE_AND_THREE_COLUMNS_TWO_LINES = 'TITLE_AND_THREE_COLUMNS_TWO_LINES'
    TITLE_AND_THREE_COLUMNS = 'TITLE_AND_THREE_COLUMNS'
    TITLE_EIGHT_COLUMNS_TWO_LINES = 'TITLE_EIGHT_COLUMNS_TWO_LINES'

    RECOMENDACAO_PESO_IDADE = 'RECOMENDACAO_PESO_IDADE'
    RECOMENDACAO_FILHOTES_ADULTOS_LINES = 'RECOMENDACAO_FILHOTES_ADULTOS_LINES'
    RECOMENDACAO_FILHOTES_ADULTOS_THREE_COLUMNS = 'RECOMENDACAO_FILHOTES_ADULTOS_THREE_COLUMNS'
    RECOMENDACAO_UM_PESO = 'RECOMENDACAO_UM_PESO'
    RECOMENDACAO_FILHOTES_ADULTOS_NO_LINES = 'RECOMENDACAO_FILHOTES_ADULTOS_NO_LINES'

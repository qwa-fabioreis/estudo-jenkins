from __future__ import annotations
from ...enums.tables_enum import TableType
from .three_columns_process import ThreeColumnsProcessor

from .title_and_n_lines_same_columns_process import TitleAndNLinesSameColumnsProcessor
from .recomendacao_tamanho_idade_process import RecomendacaoTamanhoIdadeProcessor
from .title_and_three_columns_and_two_lines_process import TitleAndThreeColumnsAndTwoLinesProcessor

from .title_and_four_columns_in_four_lines_process import TitleAndFourColumnsInFourLinesProcessor
from .recomendacao_peso_idade_five_col_process import RecomendacaoPesoIdadeFiveColProcessor
from .full_table_process import FullTableProcessor
from .recomendacao_peso_idade_six_col_process import RecomendacaoPesoIdadeSixColProcessor
from .niveis_garantia_colunas_variadas_process import NiveisGarantiaColunasVariadasProcessor
from .title_eight_columns_two_lines_same_columns_process import TitleEightColumnsAndTwoLinesSameColumnsProcessor
from .recomendacao_filhotes_adultos_three_columns_process import RecomendacaoFilhotesAdultosThreeColumnsProcessor
from .recomendacao_filhotes_adultos_lines_process import RecomendacaoFilhotesAdultosLinesProcessor
from .recomendacao_filhotes_adultos_no_lines_process import RecomendacaoFilhotesAdultosNoLinesProcessor
from .title_and_three_columns_process import TitleAndThreeColumnsProcessor
from .recomendacao_um_peso_process import RecomendacaoUmPesoProcessor


class TableProcessorCreator():

    @staticmethod
    def create(table_type):

        new_instance = None

        if table_type == TableType.TITLE_AND_THREE_COLUMNS:
            new_instance = TitleAndThreeColumnsProcessor()

        elif table_type == TableType.TITLE_N_LINES_SAME_COLUMNS:
            new_instance = TitleAndNLinesSameColumnsProcessor()

        elif table_type == TableType.THREE_COLUMNS:
            new_instance = ThreeColumnsProcessor()

        elif table_type == TableType.RECOMENDACAO_TAMANHO_IDADE:
            new_instance = RecomendacaoTamanhoIdadeProcessor()

        elif table_type == TableType.TITLE_AND_THREE_COLUMNS_TWO_LINES:
            new_instance = TitleAndThreeColumnsAndTwoLinesProcessor()

        elif table_type == TableType.TITLE_FOUR_COLUMNS_IN_FOUR_LINES:
            new_instance = TitleAndFourColumnsInFourLinesProcessor()

        elif table_type == TableType.RECOMENDACAO_PESO_IDADE_FIVE_COL:
            new_instance = RecomendacaoPesoIdadeFiveColProcessor()

        elif table_type == TableType.RECOMENDACAO_PESO_IDADE_SIX_COL:
            new_instance = RecomendacaoPesoIdadeSixColProcessor()

        elif table_type == TableType.FULL_TABLE:
            new_instance = FullTableProcessor()

        elif table_type == TableType.NIVEIS_GARANTIA_COLUNAS_VARIADAS:
            new_instance = NiveisGarantiaColunasVariadasProcessor()

        elif table_type == TableType.TITLE_EIGHT_COLUMNS_TWO_LINES:
            new_instance = TitleEightColumnsAndTwoLinesSameColumnsProcessor()

        elif table_type == TableType.RECOMENDACAO_FILHOTES_ADULTOS_THREE_COLUMNS:
            new_instance = RecomendacaoFilhotesAdultosThreeColumnsProcessor()

        elif table_type == TableType.RECOMENDACAO_FILHOTES_ADULTOS_LINES:
            new_instance = RecomendacaoFilhotesAdultosLinesProcessor()

        elif table_type == TableType.RECOMENDACAO_UM_PESO:
            new_instance = RecomendacaoUmPesoProcessor()

        elif table_type == TableType.RECOMENDACAO_FILHOTES_ADULTOS_NO_LINES:
            new_instance = RecomendacaoFilhotesAdultosNoLinesProcessor()

        return new_instance

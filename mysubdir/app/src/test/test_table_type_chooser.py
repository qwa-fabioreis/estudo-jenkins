import unittest
from ..text.table_type_chooser import choose_table_type
from ..enums.tables_enum import TableType


class TestTableType(unittest.TestCase):

    def test_choose_table_type_title_and_three_columns(self):
        table = {'213': [[370, 213, 630, 41]],
                 '258': [[370, 258, 244, 282], [618, 258, 184, 282], [806, 258, 194, 282]]}
        table_type = choose_table_type(table)
        self.assertEqual(table_type, TableType.TITLE_AND_THREE_COLUMNS)

    def test_choose_table_recomendacao_peso_idade_six_col(self):
        table = {'644': [[370, 644, 630, 34]], '684': [[372, 684, 149, 32], [528, 684, 472, 12]],
                 '705': [[528, 705, 91, 11], [623, 705, 91, 11], [718, 705, 91, 11], [813, 705, 91, 11],
                         [908, 705, 92, 11]],
                 '723': [[370, 723, 154, 49], [528, 723, 91, 49], [623, 723, 91, 49], [718, 723, 91, 49],
                         [813, 723, 91, 49],
                         [908, 723, 92, 49]],
                 '776': [[370, 776, 154, 73], [528, 776, 91, 73], [623, 776, 91, 73], [718, 776, 91, 73],
                         [813, 776, 91, 73],
                         [908, 776, 92, 73]],
                 '853': [[370, 853, 154, 75], [528, 853, 91, 75], [623, 853, 91, 75], [718, 853, 91, 75],
                         [813, 853, 91, 75],
                         [908, 853, 92, 75]]}
        table_type = choose_table_type(table)
        self.assertEqual(table_type, TableType.RECOMENDACAO_PESO_IDADE_SIX_COL)

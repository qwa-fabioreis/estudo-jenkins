from .general_extractor import GeneralExtractor
from ...enums.facas_enum import Faca
from ...exceptions.CustomException import NotSupportedException


def create_extractor(img, faca):
    extractor = None

    if Faca[faca] in (Faca.CANGURU_PREMIER_NATTU_CAES_101KG,):
        extractor_class = GeneralExtractor(225, 305, 626, 2214, 1647, 2048, 626, 2216, 1647, 2575, 626,
                                           305, 1647, 1344, 626, 1344, 1647, 1747, 2048, 305, 3067, 1014, 1014, 1706, 2048, 1706, 2224)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_NATTU_CAES_12KG,):
        extractor_class = GeneralExtractor(265, 305, 674, 2306, 1774, 2183, 674, 2280, 1774, 2593, 674,
                                           305, 1774, 1374, 674, 1374, 1774, 1803, 2183, 305, 3183, 994, 994, 1764, 2183, 1764, 2337)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_NATTU_GATOS_75KG,):
        extractor_class = GeneralExtractor(195, 253, 470, 2074, 1410, 1685, 470, 2068, 1410, 2289, 470,
                                           253, 1410, 1264, 470, 1264, 1410, 1625, 1685, 253, 2614, 1002, 1002, 1569, 1685, 1569, 2070)

    elif Faca[faca] in (Faca.CANGURU_GOLDEN_FORMULA_CAES_15KG,):
        extractor_class = GeneralExtractor(235, 425, 726, 2534, 1767, 2258, 726, 2556, 3313, 2761, 726,
                                           425, 1767, 1410, 726, 1410, 1767, 2031, 2258, 425, 3311, 1182, 1182, 2029, 2258, 2029, 2550)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_AMBIENTES_INTERNOS_75KG,):
        extractor_class = GeneralExtractor(191, 639, 476, 2322, 1437, 1722, 476, 2332, 1437, 2553, 476,
                                           639, 1437, 1540, 476, 1540, 1437, 1857, 1716, 639, 2651, 1218, 1218, 1879, 1716, 1879, 2342)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_AMBIENTES_INTERNOS_12KG,):
        extractor_class = GeneralExtractor(217, 489, 617, 2369, 1698, 2098, 621,  2370, 1702, 2705, 617,
                                           489, 1698, 1478, 617, 1478, 1698, 1839, 2098, 489, 3183, 1054, 1054, 1907, 2098, 1907, 2392)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_FORMULA_15KG,):
        extractor_class = GeneralExtractor(377, 561, 804, 2596, 1969, 2396, 804, 2586, 1969, 2860, 804,
                                           561, 1969, 1640, 804, 1640, 1969, 2049, 2396, 561, 3571, 1236, 1236, 2059, 2396, 2059, 2594)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_FORMULA_20KG,):
        extractor_class = GeneralExtractor(341, 623, 778, 2778, 2033, 2470, 797, 2792, 2052, 3121, 778,
                                           623, 2033, 1738, 778, 1738, 2033, 2187, 2470, 623, 3767, 1334, 1334, 2223, 2470, 2223, 2562)

    elif Faca[faca] in (Faca.CANGURU_GOLDEN_FORMULA_CAES_101,):
        extractor_class = GeneralExtractor(329, 469, 658, 2446, 1697, 2017, 329, 2464, 3073, 2643, 657,
                                           469, 1705, 1326, 657, 1325, 1705, 1961, 2100, 469, 3065, 1149, 1149, 1966, 2100, 1966, 2471)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_RACAS_ESPECIFICAS_75KG,):
        extractor_class = GeneralExtractor(189, 621, 470, 2324, 1411, 1692, 470, 2348, 1411, 2551, 470,
                                           621, 1411, 1566, 470, 1566, 1411, 1897, 1692, 621, 2633, 1238, 1238, 1893, 1692, 1893, 2336)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_RAÇAS_ESPECIFICAS_12KG,):
        extractor_class = GeneralExtractor(211, 491, 612, 2366, 1689, 2090, 612, 2359, 1689, 2680, 612,
                                           491, 1689, 1475, 612, 1475, 1689, 1854, 2090, 491, 3167, 1054, 1054, 1903, 2090, 1903, 2382)

    elif Faca[faca] in (Faca.CANGURU_VITTA_NATURAL_CAES_6KG,):
        extractor_class = GeneralExtractor(287, 801, 574, 2372, 1467, 1754, 574, 2400, 1468, 2589, 574,
                                           801, 1467, 1804, 574, 1804, 1467, 2041, 1754, 801, 2653, 1308, 1308, 1927, 1754, 1927, 2220)

    elif Faca[faca] in (Faca.CANGURU_VITTA_NATURAL_CAES_101KG,):
        extractor_class = GeneralExtractor(190, 325, 509, 2481, 1557, 1877, 190, 2309, 2931, 2497, 509,
                                           325, 1557, 1549, 509, 1549, 1557, 1849, 1877, 325, 2917, 969, 969, 1785, 1897, 1785, 2309)

    elif Faca[faca] in (Faca.CANGURU_VITTA_NATURAL_CAES_15KG,):
        extractor_class = GeneralExtractor(171, 367, 640, 2510, 1705, 2174, 640, 2508, 3257, 2707, 640,
                                           367, 1705, 1706, 640, 1706, 1705, 2021, 2174, 367, 3239, 1130, 1130, 1947, 2174, 1947, 2500)

    elif Faca[faca] in (Faca.CANGURU_VITTA_NATURAL_GATOS_101KG,):
        extractor_class = GeneralExtractor(183, 329, 500, 2209, 1574, 1891, 500, 2305, 2925, 2485, 500,
                                           329, 1574, 1559, 500, 1559, 1574, 1852, 1891, 329, 2950, 974, 974, 1793, 1891, 1793, 2308)

    elif Faca[faca] in (Faca.CANGURU_PREMIER_AMBIENTES_INTERNOS_25KG,):
        extractor_class = GeneralExtractor(1249, 1977, 1593, 3025, 1593, 1928, 393, 3065, 1081, 3385,
                                           393, 1887, 1081, 2489, 393, 2489, 1081, 2705, 393, 1369, 1081, 1793, 943, 1362, 395, 657, 943)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_FORMULA_3KG,):
        extractor_class = GeneralExtractor(445, 980, 825, 2155, 825, 1205, 1845, 3175, 2570, 3560, 1845,
                                           1855, 2570, 2430, 1845, 2430, 2570, 2850, 1845, 1340, 2570, 1855, 910, 1340, 1845, 540, 910)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_FORMULA_1KG,):
        extractor_class = GeneralExtractor(520, 670, 842, 1525, 842, 1165, 1825, 2465, 2345, 2800, 1825,
                                           1475, 2345, 1950, 1825, 1950, 2345, 2190, 1825, 1060, 2345, 1490, 750, 1060, 1825, 480, 750)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_SELECAO_NATURAL_CAES_1KG,):
        extractor_class = GeneralExtractor(520, 670, 842, 1520, 842, 1165, 1825, 2465, 2345, 2800, 1825,
                                           1475, 2345, 1930, 1825, 1930, 2345, 2185, 1825, 1145, 2345, 1475, 760, 1145, 1825, 480, 760)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_SELECAO_NATURAL_CAES_3KG,):
        extractor_class = GeneralExtractor(445, 980, 825, 2165, 825, 1205, 1845, 3175, 2565, 3570, 1845,
                                           1860, 2565, 2450, 1845, 2450, 2565, 2780, 1845, 1495, 2565, 1860, 925, 1495, 1845, 540, 925)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_SELECAO_NATURAL_GATOS_3KG,):
        extractor_class = GeneralExtractor(460, 1080, 840, 2205, 840, 1220, 1860, 3215, 2585, 3610, 1860,
                                           1950, 2585, 2500, 1860, 2500, 2585, 2800, 1860, 1610, 2585, 1950, 1040, 1610, 1860, 690, 1040)

    elif Faca[faca] in (Faca.FINEPACK_GOLDEN_SELECAO_NATURAL_GATOS_1KG,):
        extractor_class = GeneralExtractor(520, 670, 842, 1530, 842, 1165, 1830, 2465, 2355, 2805, 1830,
                                           1470, 2355, 1935, 1830, 1935, 2355, 2180, 1830, 1150, 2355, 1470, 760, 1150, 1830, 480, 760)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_AMBIENTES_INTERNOS_1KG,):
        extractor_class = GeneralExtractor(515, 485, 840, 1345, 840, 1165, 1825, 2280, 2350, 2625, 1825,
                                           1335, 2350, 1850, 1825, 1850, 2350, 1990, 1825, 915, 2350, 1250, 555, 915, 1825, 300, 555)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_AMBIENTES_INTERNOS_25KG,):
        extractor_class = GeneralExtractor(445, 710, 782, 1780, 782, 1120, 1845, 2790, 2525, 3145, 1845,
                                           1630, 2525, 2230, 1845, 2230, 2525, 2430, 1845, 1120, 2525, 1545, 690, 1120, 1845, 380, 690)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_FORMULA_1KG,):
        extractor_class = GeneralExtractor(520, 525, 842, 1375, 842, 1165, 1830, 2325, 2350, 2665, 1830,
                                           1380, 2350, 1900, 1830, 1900, 2350, 2075, 1830, 945, 2350, 1285, 585, 945, 1830, 340, 585)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_FORMULA_25KG,):
        extractor_class = GeneralExtractor(447, 710, 784, 1770, 784, 1122, 1845, 2801, 2525, 3145, 1845,
                                           1625, 2525, 2237, 1845, 2237, 2525, 2441, 1845, 1140, 2525, 1540, 675, 1140, 1845, 380, 675)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_NATTU_CAES_1KG,):
        extractor_class = GeneralExtractor(505, 475, 830, 1335, 830, 1155, 1815, 2270, 2340, 2615, 1815, 
                                           1280, 2340, 1780, 1815, 1780, 2340, 1960, 1815, 895, 2340, 1280, 545, 895, 1815, 290, 545)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_NATTU_CAES_25KG,):
        extractor_class = GeneralExtractor(435, 700, 772, 1780, 772, 1110, 1835, 2780, 2515, 3135, 1835,
                                           1575, 2515, 2160, 1835, 2160, 2515, 2395, 1835, 1120, 2515, 1575, 675, 1120, 1835, 370, 675)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_NATTU_GATOS_15KG,):
        extractor_class = GeneralExtractor(465, 710, 802, 1625, 802, 1140, 2050, 2480, 2655, 2830, 2050,
                                           1430, 2655, 2000, 2050, 2000, 2655, 2150, 2050, 1085, 2655, 1430, 670, 1085, 2050, 380, 670)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_RACAS_ESPECIFICAS_1KG,):
        extractor_class = GeneralExtractor(515, 485, 837, 1345, 837, 1160, 1825, 2285, 2350, 2625, 1825,
                                           1335, 2350, 1850, 1825, 1850, 2350, 2030, 1825, 915, 2350, 1250, 560, 915, 1825, 300, 560)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_RACAS_ESPECIFICAS_25KG,):
        extractor_class = GeneralExtractor(445, 710, 782, 1780, 782, 1120, 1850, 2790, 2530, 3145, 1850,
                                           1630, 2530, 2245, 1850, 2245, 2530, 2480, 1850, 1150, 2530, 1545, 685, 1150, 1850, 380, 685)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_SELECAO_NATURAL_CAES_1KG,):
        extractor_class = GeneralExtractor(505, 475, 830, 1330, 830, 1155, 1815, 2275, 2340, 2615, 1815,
                                           1325, 2340, 1800, 1815, 1800, 2340, 2000, 1815, 910, 2340, 1250, 540, 910, 1815, 290, 540)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_SELECAO_NATURAL_CAES_25KG,):
        extractor_class = GeneralExtractor(721, 1041, 1065, 2103, 1065, 1400, 2121, 3105, 2800, 3449, 2121,
                                           1952, 2800, 2497, 2121, 2497, 2800, 2768, 2121, 1481, 2800, 1841, 1022, 1479, 2121, 705, 1022)

    elif Faca[faca] in (Faca.FINEPACK_PREMIER_SELECAO_NATURAL_GATOS_15KG,):
        extractor_class = GeneralExtractor(885, 1295, 1225, 2205, 1225, 1561, 2470, 3060, 3065, 3410, 2470,
                                           2060, 3065, 2540, 2470, 2540, 3065, 2755, 2470, 1620, 3065, 1975, 1225, 1620, 2470, 960, 1225)

    elif Faca[faca] in (Faca.FINEPACK_VITTA_NATURAL_GATOS_3KG,):
        extractor_class = GeneralExtractor(1657, 445, 2033, 1565, 2033, 2413, 469, 2933, 1193, 3313,
                                           469, 1673, 1193, 2253, 469, 2253, 1193, 2716, 469, 1280, 1193, 1673, 771, 1280, 469, 461, 771)

    elif Faca[faca] in (Faca.FINEPACK_VITTA_NATURAL_CAES_3KG,):
        extractor_class = GeneralExtractor(449, 977, 825, 2169, 825, 1205, 1849, 3173, 2565, 3573, 1849,
                                           1857, 2565, 2451, 1849, 2451, 2565, 2957, 1849, 1307, 2565, 1857, 887, 1307, 1849, 537, 887)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_GATOS_101KG,):
        extractor_class = GeneralExtractor(315, 470, 650, 2645, 1700, 2020, 315, 2460, 2780, 2645, 650,
                                           470, 1700, 1415, 650, 1415, 1700, 1980, 2010, 470, 3090, 1337, 1337, 1960, 2010, 1960, 2475)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_GATOS_1KG,):
        extractor_class = GeneralExtractor(990, 1700, 1340, 2520, 1340, 1685, 330, 2555, 855, 2910,
                                           330, 1560, 855, 2025, 330, 2025, 855, 2295, 330, 1135, 855, 1530, 845, 1135, 330, 550, 845)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_GATOS_3KG,):
        extractor_class = GeneralExtractor(1320, 2160, 1720, 3250, 1720, 2125, 450, 3255, 1170, 3670, 450,
                                           1990, 1170, 2545, 450, 2545, 1170, 2920, 450, 1455, 1170, 1990, 1060, 1455, 450, 710, 1060)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_RACAS_ESPECIFICAS_1KG,):
        extractor_class = GeneralExtractor(1010, 1675, 1340, 2495, 1340, 1668, 330, 2530, 855, 2870,
                                           330, 1575, 855, 2100, 330, 2100, 855, 2270, 330, 1155, 855, 1490, 800, 1155, 330, 545, 800)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_RACAS_ESPECIFICAS_25KG,):
        extractor_class = GeneralExtractor(450, 710, 785, 1780, 785, 1120, 1850, 2790, 2530, 3140, 1850,
                                           1625, 2530, 2230, 1850, 2230, 2530, 2450, 1850, 1120, 2530, 1540, 695, 1120, 1850, 380, 695)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_SELECAO_NATURAL_CAES_101KG,):
        extractor_class = GeneralExtractor(190,	505, 515, 2485,	1555, 1875,	190, 2490, 2930, 2685, 515,	
                                            505, 1555, 1420, 515, 1420,	1555, 1910,1875, 505, 2930, 1140, 1140, 1940, 1875,	1940, 2490)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_SELECAO_NATURAL_GATOS_75KG,):
        extractor_class = GeneralExtractor(190, 625, 485, 2355, 1420, 1715, 190, 2355, 2455, 2565, 485,
                                           625, 1420, 1505, 485, 1505, 1420, 1850, 1715, 625, 2645, 1180, 1180, 1865, 1715, 1865, 2355)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_SELECAO_NATURAL_CAES_12KG,):
        extractor_class = GeneralExtractor(215, 650, 630, 2505, 1705, 2120, 215, 2505, 2980, 2825, 630,
                                           650, 1705, 1590, 630, 1590, 1705, 1960, 2120, 650, 3190, 1225, 1225, 1990, 2120, 1990, 2505)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_RACAS_ESPECIFICAS_12KG,):
        extractor_class = GeneralExtractor(210, 630, 625, 2510, 1700, 2115, 210, 2510, 2975, 2830, 625,
                                           630, 1700, 1610, 625, 1610, 1700, 1920, 2115, 630, 3190, 1290, 1290, 2025, 2115, 2025, 2510)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_RACAS_ESPECIFICAS_75KG,):
        extractor_class = GeneralExtractor(190, 625, 485, 2565, 1420, 1715, 190, 2355, 2645, 2565, 485,
                                           625, 1420, 1325, 485, 1325, 1420, 1840, 1715, 625, 2645, 1160, 1160, 1910, 1715, 1910, 2355)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_GATOS_75KG,):
        extractor_class = GeneralExtractor(190,	625, 485, 2565,	1420, 1705,	190, 2325, 1940, 2565, 485,	
                                            625, 1420, 1330, 485, 1330,	1420, 1850,	1705, 625, 2645, 1110, 1110, 1915, 1705, 1915, 2325)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_SELECAO_NATURAL_GATOS_101KG,):
        extractor_class = GeneralExtractor(190, 505, 515, 2680, 1555, 1875, 190, 2480, 2180, 2680, 515,
                                           505, 1555, 1420, 515, 1420, 1555, 1870, 1875, 505, 2930, 1065, 1065, 1940, 1875, 1940, 2480)

    elif Faca[faca] in (Faca.INCOPLAST_PREMIER_SELECAO_NATURAL_CAES_101KG,):
        extractor_class = GeneralExtractor(265, 600, 690, 2390, 1710, 2135, 265, 2390, 2890, 2730, 690,
                                           600, 1710, 1505, 690, 1505, 1710, 1870, 2135, 600, 3155, 1180, 1180, 1920, 2135, 1920, 2390)

    elif Faca[faca] in (Faca.INCOPLAST_GOLDEN_SELECAO_NATURAL_CAES_12KG,):
        extractor_class = GeneralExtractor(415, 700, 830, 3005, 1905, 2300, 415, 2795, 2980, 3010, 830,
                                           700, 1910, 1680, 830, 1680, 1910, 2210, 2300, 700, 3395, 1260, 1260, 2215, 2300, 2215, 2795)

    elif Faca[faca] in (Faca.ZARAPLAST_PREMIER_GATOS_15KG,):
        extractor_class = GeneralExtractor(1120, 1410, 1435, 2350, 1435, 1750, 285, 2340, 900, 2700,
                                           285, 1275, 900, 1730, 285, 1730, 900, 2040, 285, 840, 900, 1205, 430, 840, 285, 135, 430)

    elif Faca[faca] in (Faca.ZARAPLAST_PREMIER_GATOS_500G,):
        extractor_class = GeneralExtractor(1030, 1130, 1280, 1810, 1280, 1540, 290, 1840, 790, 2140,
                                           290, 1016, 790, 1365, 290, 1365, 790, 1620, 290, 695, 790, 960, 365, 695, 290, 140, 365)

    if Faca[faca].value[1] == 'INTEIRA':
        extractor = extractor_class.extract_inteira(img)

    elif Faca[faca].value[1] == 'ABERTA':
        extractor = extractor_class.extract_aberta(img)

    else:
        raise NotSupportedException(400, 'Faca %s ainda nao suportada' % faca)

    return extractor

from algClasses.genetic_algorithm import SimpleGeneticAlgorithm
from algClasses.genetic_algorithm import CellGeneticAlgorithm
from algClasses.genetic_algorithm import IslandGeneticAlgorithm

count_before_end = 1000  # количество поколений с одинаковой лучшей хромосомой


def run_alg(variables: dict):
    """
    Прогоняет алгоритм с выбранными параметрами.
    :param variables: Словарь. Содержит в себе название алгоритма, массив с параметрами,
    :return:
    """
    if variables["methode"] == "SimpleGenVal":
        start_simple_alg()
    elif variables["methode"] == "CellGenAlg":
        start_cell_alg()
    elif variables["methode"] == "IslandGenAlg":
        start_island_alg()


def start_simple_alg():
    pass


def start_cell_alg():
    pass


def start_island_alg():
    pass

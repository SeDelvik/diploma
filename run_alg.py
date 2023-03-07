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
    # в сбор данных должны входить:
    # алгоритм и использованные параметры
    # лучшая приспособленность
    # кол-во поколений (для островов учитываются только сколько раз острова обменивались)
    # время выполнения (желательно но не обязательно.)
    gen_alg = get_alg_obj(variables)
    k = 0
    best_fit = gen_alg.bestChromosome.fit
    while True:
        if k > count_before_end:  # дописать внятный сборщик данных
            break
        gen_alg.one_cycle()
        if gen_alg.bestChromosome.fit > best_fit:
            k = 0
            best_fit = gen_alg.bestChromosome.fit
        else:
            k += 1


def get_alg_obj(variables: dict):
    gen_alg = None
    if variables["methode"] == "SimpleGenVal":
        gen_alg = SimpleGeneticAlgorithm(variables["src"], variables["operators"], variables["population_count"],
                                         variables["probability"])
    elif variables["methode"] == "CellGenAlg":
        gen_alg = CellGeneticAlgorithm(variables["population_count"], variables["src"], variables["operators"])
    elif variables["methode"] == "IslandGenAlg":
        gen_alg = IslandGeneticAlgorithm(variables["src"], variables["island_count"], variables["population_count"],
                                         variables["count_generations"], variables["count_person_in_swap"])
    return gen_alg

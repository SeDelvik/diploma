import copy
import json
from datetime import datetime
import time

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
    data = copy.deepcopy(variables)  # для сбора данных
    start_time = datetime.now()  # для расчета времени выполнения
    all_best_fits = []

    gen_alg = get_alg_obj(variables)
    k = 0
    best_fit = gen_alg.bestChromosome.fit
    while True:
        if k > count_before_end:  # дописать внятный сборщик данных
            break
        gen_alg.one_cycle()
        all_best_fits.append(gen_alg.bestChromosome.fit)
        print(f"fit:{gen_alg.bestChromosome.fit}")
        if gen_alg.bestChromosome.fit > best_fit:
            k = 0
            best_fit = gen_alg.bestChromosome.fit
        else:
            k += 1
    data["execution_time"] = str(datetime.now() - start_time)
    data["fits_in_all_time"] = all_best_fits
    data["best_chromosome"] = gen_alg.bestChromosome.chromosome
    create_output_data(data)


def get_alg_obj(variables: dict):
    gen_alg = None
    if variables["methode"] == "SimpleGenVal":
        tmp = SimpleGeneticAlgorithm(src=variables["src"], operator=variables["operators"],
                                     population_count=variables["population_count"],
                                     probability=variables["probability"])
        gen_alg = tmp
    elif variables["methode"] == "CellGenAlg":
        gen_alg = CellGeneticAlgorithm(population_count=variables["population_count"], src=variables["src"],
                                       operator=variables["operators"])
    elif variables["methode"] == "IslandGenAlg":
        gen_alg = IslandGeneticAlgorithm(src_doc=variables["src"], count_island=variables["island_count"],
                                         one_island_population_count=variables["population_count"],
                                         count_generation=variables["count_generations"],
                                         count_person_in_swap=variables["count_person_in_swap"])
    return gen_alg

    # в сбор данных должны входить:
    # алгоритм и использованные параметры
    # лучшая приспособленность
    # кол-во поколений (для островов учитываются только сколько раз острова обменивались)
    # время выполнения (желательно но не обязательно.)


def create_output_data(data: dict):
    with open(f'./output/{datetime.now().strftime("%d-%m-%Y_%S-%M-%H")}.json', 'w+') as fp:
        json.dump(data, fp)

import json
import random

from algClasses.task import Task
from run_alg import run_alg


def create_dataset(file_name: str, max_cost: int, execute_time: int, count: int):
    """
    Генератор данных для алгоритма.
    :param file_name: имя конечного файла
    :param max_cost: максимальная цена таска
    :param count: количество тасков в файле
    :param execute_time: максимальное время выполнения задачи
    :return:
    """
    arr_execute_time = []
    for i in range(count):
        arr_execute_time.append(random.randint(1, execute_time))

    max_deadline = sum(arr_execute_time, start=0)


    arr = []
    for i in range(count):
        # tmp_time = arr_execute_time[i] # random.randint(1, max_deadline)
        tmp_cost = random.randint(1, max_cost)
        tmp_deadline = random.randint(arr_execute_time[i], max_deadline)
        tmp_name = i
        task_tmp = Task(arr_execute_time[i], tmp_cost, tmp_deadline, tmp_name)
        arr.append(task_tmp.to_JSON())

    with open(f'./res/{file_name}.json', 'w+') as fp:
        json.dump(arr, fp)


def get_potential_max_cost(file_name: str) -> int:
    """
    Считает примерную максимальную цену датасета.
    :param file_name: Путь до файла.
    :return: Возможная максимальна стоимость.
    """
    task_list = []
    with open(file_name, 'r') as fp:
        tmp_task_data = json.load(fp)
        for task1 in tmp_task_data:
            try:
                tmp_task = Task(task1["time"], task1["cost"], task1["deadline"],
                                task1["name"])
            except:
                tmp_task = Task(task1["time"], task1["cost"], task1["deadline"],
                                "task")
            task_list.append(tmp_task)
    task_list.sort(key=lambda tsk: tsk.cost, reverse=True)

    tmp_time = 0
    cost = 0
    for task in task_list:
        if task.time + tmp_time <= task.deadline:
            tmp_time += task.time
            cost += task.cost
    return cost


def run_all_variation_algs():
    algorythms = ["SimpleGenAlg", "CellGenAlg", "IslandGenAlg"]
    parent_choise = [0, 1, 2]
    recombinations = [0, 1, 2]
    mutations = [0, 1, 2]
    selections = [0, 1, 2]
    population_count = 100
    probability = 0.5
    island_count = 10
    count_generations = 10
    count_person_in_swap = 10

    variables = {}
    variables["src"] = "./res/randomTask100_1.json"
    # for alg_name in algorythms:
    # обычный алгоритм
    for parent in parent_choise:
        for recombination in recombinations:
            for mutation in mutations:
                for selection in selections:
                    # выбор родителей, рекмбинация, мутация, создание новой популяции
                    arr_params = [parent, recombination, mutation, selection]
                    variables["methode"] = algorythms[0]  # алгоритм
                    variables["operators"] = arr_params
                    variables["population_count"] = population_count
                    variables["probability"] = probability
                    variables["island_count"] = island_count
                    variables["count_generations"] = count_generations
                    variables["count_person_in_swap"] = count_person_in_swap
                    run_alg(variables)
    #  ячеистый
    for recombination in recombinations:
        for mutation in mutations:
            # выбор родителей, рекмбинация, мутация, создание новой популяции
            arr_params = [parent_choise[0], recombination, mutation, selections[0]]
            variables["methode"] = algorythms[1]  # алгоритм
            variables["operators"] = arr_params
            variables["population_count"] = population_count
            variables["probability"] = probability
            variables["island_count"] = island_count
            variables["count_generations"] = count_generations
            variables["count_person_in_swap"] = count_person_in_swap
            run_alg(variables)
    #  островной
    arr_params = [parent_choise[0], recombinations[0], mutations[0], selections[0]]
    variables["methode"] = algorythms[2]  # алгоритм
    variables["operators"] = arr_params
    variables["population_count"] = population_count
    variables["probability"] = probability
    variables["island_count"] = island_count
    variables["count_generations"] = count_generations
    variables["count_person_in_swap"] = count_person_in_swap
    run_alg(variables)


if __name__ == '__main__':
    # create_dataset("randomTask100_1", 10, 30, 100)
    # print(get_potential_max_cost("./res/testTask.json"))
    run_all_variation_algs()

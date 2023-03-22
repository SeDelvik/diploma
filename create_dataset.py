import json
import random

from algClasses.task import Task


def create_dataset(file_name: str, max_cost: int, max_deadline: int, count: int):
    """
    Генератор данных для алгоритма.
    :param file_name: имя конечного файла
    :param max_cost: максимальная цена таска
    :param max_deadline: максимальный дедлайн таска
    :param count: количество тасков в файле
    :return:
    """
    arr = []
    for i in range(count):
        tmp_time = random.randint(1, max_deadline)
        tmp_cost = random.randint(1, max_cost)
        tmp_deadline = random.randint(1, max_deadline)
        tmp_name = f"task{i}"
        task_tmp = Task(tmp_time, tmp_cost, tmp_deadline, tmp_name)
        arr.append(task_tmp.to_JSON())

    with open(f'./res/{file_name}.json', 'w+') as fp:
        json.dump(arr, fp)


if __name__ == '__main__':
    create_dataset("testTask2", 10, 100, 5)

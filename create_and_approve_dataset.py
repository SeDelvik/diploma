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


if __name__ == '__main__':
    # create_dataset("testTask2", 10, 100, 5)
    print(get_potential_max_cost("./res/testTaskList.json"))

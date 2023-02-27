import json
import random
import algClasses.task as task


class Chromosome:
    task_list = []

    def __init__(self, path=''):
        if len(self.task_list) < 1:
            self.create_task_list(path)
        self.chromosome = self.create_random_chromosome(len(self.task_list))
        self.fit = 0
        self.count_self_fit()


    # инициализация статического массива задач
    @staticmethod
    def create_task_list(path):
        with open(path, 'r') as fp:
            tmp_task_data = json.load(fp)
            for task1 in tmp_task_data:
                tmp_task = task.Task(task1["time"], task1["cost"], task1["deadline"], task1["name"]) #todo создать проверку на то что имя не существует
                Chromosome.task_list.append(tmp_task)


    # создание случайной хромосомы
    def create_random_chromosome(self, length):
        arr = []
        for i in range(length):
            arr.append(random.randint(0, 1))
        return arr

    # подсчет собственной приспособленности
    def count_self_fit(self):
        pass

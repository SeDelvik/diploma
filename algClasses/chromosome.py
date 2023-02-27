import json
import random
import algClasses.task as task


class Chromosome:
    task_list = []  # массив, хранящий обьекты-задачи. нужен для расчета приспособленности хромосомы.

    def __init__(self, path=''):
        if len(self.task_list) < 1:
            self.create_task_list(path)
        self.chromosome = self.create_random_chromosome(len(self.task_list))
        self.fit = 0
        self.count_self_fit()

    def __str__(self):
        return f"fit: {self.fit}, chromosome: {self.chromosome}"

    @staticmethod
    def create_task_list(path):
        """инициализирует статический массив задач."""
        with open(path, 'r') as fp:
            tmp_task_data = json.load(fp)
            for task1 in tmp_task_data:
                # todo проверка на валидность тасков в json. пока обрабатывается только имя и то неправильно
                try:
                    tmp_task = task.Task(task1["time"], task1["cost"], task1["deadline"],
                                         task1["name"])
                except:
                    tmp_task = task.Task(task1["time"], task1["cost"], task1["deadline"],
                                         "task")
                Chromosome.task_list.append(tmp_task)
        Chromosome.task_list.sort(key=lambda tsk: tsk.deadline)

    def create_random_chromosome(self, length):
        """Создает случайную хромосому"""
        arr = []
        for i in range(length):
            arr.append(random.randint(0, 1))
        return arr

    def count_self_fit(self):  # проверялось на int времени. что будет на date не известно
        """Считает приспособленность хромосомы."""
        last_time = 0
        final_cost = 0
        for i in range(len(self.chromosome)):
            if self.chromosome[i] == 0:
                continue
            if last_time + self.task_list[i].time <= self.task_list[
                i].deadline:  # укладывается ли выбранная задача в расписание
                last_time += self.task_list[i].time
                final_cost += self.task_list[i].cost
            else:
                final_cost = 0
                break
        self.fit = final_cost


    #--------------------------
    # операторы рекомбинации
    #--------------------------

def one_point_croossingover(parent1,parent2,cut_point):
    arr1 = []
    arr2 = []
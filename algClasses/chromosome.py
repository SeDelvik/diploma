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

    # --------------------------
    # операторы рекомбинации
    # --------------------------

    def one_point_croossingover(parent1, parent2, cut_point):
        """
        Применяет одноточечный кроссинговер. Возвращает 2 новые хромосомы-потомка
        :param parent1: Хромосома-родитель1
        :param parent2: Хромосома-родитель2
        :param cut_point: точка разреза
        :type parent1: Chromosome
        :type parent2: Chromosome
        :type cut_point: int
        :return: Массив с двумя хромосомами-потомками
        :rtype: list
        """
        arr1 = parent1.chromosome[:cut_point] + parent2.chromosome[cut_point:]
        arr2 = parent2.chromosome[:cut_point] + parent1.chromosome[cut_point:]
        chrom1 = Chromosome()
        chrom2 = Chromosome()
        chrom1.chromosome = arr1
        chrom2.chromosome = arr2
        return [chrom1, chrom2]

    def two_point_crossingover(parent1, parent2, first_cut_point, second_cut_point):
        """
        Применяет одноточечный кроссинговер. Возвращает 2 новые хромосомы-потомка. Если первая точка дальеш чем вторая -
            меняет их местами.
        :param parent1: Хромосома-родитель1
        :param parent2: Хромосома-родитель2
        :param first_cut_point: первая точка разреза
        :param second_cut_point: вторая точка разреза
        :type parent1: Chromosome
        :type parent2: Chromosome
        :type first_cut_point: int
        :type second_cut_point: int
        :return: Массив с двумя хромосомами-потомками
        :rtype: list
        """
        if first_cut_point > second_cut_point:
            tmp = first_cut_point
            first_cut_point = second_cut_point
            second_cut_point = tmp
        arr1 = parent1.chromosome[:first_cut_point] + parent2.chromosome[
                                                      first_cut_point:second_cut_point] + parent1.chromosome[
                                                                                          second_cut_point:]
        arr2 = parent2.chromosome[:first_cut_point] + parent1.chromosome[
                                                      first_cut_point:second_cut_point] + parent2.chromosome[
                                                                                          second_cut_point:]
        chrom1 = Chromosome()
        chrom2 = Chromosome()
        chrom1.chromosome = arr1
        chrom2.chromosome = arr2
        return [chrom1, chrom2]

    def binary_mask_crossingover(parent1, parent2, binary_dude):
        """
        Триадный кроссинговер. Помимо двух хромосом родителей использует
        :param parent1: хромосома-родитель1
        :type parent1: Chromosome
        :param parent2: хромосома-родитель2
        :type parent2: Chromosome
        :param binary_dude: хромосома для бинарной маски
        :type binary_dude: Chromosome
        :return: массив с двумя хромосомами потомками
        :rtype: list
        """
        arr1 = parent1.chromosome[:]
        arr2 = parent2.chromosome[:]
        for i in range(len(parent1.chromosome)):
            if binary_dude.chromosome[i] == 0:
                arr1[i] = parent2.chromosome[i]
                arr2[i] = parent1.chromosome[i]
        chr1 = Chromosome()
        chr2 = Chromosome()
        chr1.chromosome = arr1
        chr2.chromosome = arr2
        return [chr1, chr2]

    # --------------------------
    # операторы мутации
    # --------------------------

    def common_binary_mutation(self, probability):
        """
        Обычная бинарная мутация. Каждый бит может мутировать с некоторой вероятностью.
        :param probability: Вероятность мутации каждого бита. Лежит в промежутке от 0 до 1
        :type probability: float
        :return:
        """
        for i in range(len(self.chromosome)):
            if random.random() > probability:
                if self.chromosome[i] == 1:
                    self.chromosome[i] = 0
                else:
                    self.chromosome[i] = 1

    def inversion_mutation(self, start, end):
        """
        Мутация-инверсия. Участок в хромосоме, обозначенный start и end переворачивается.
        Если начало находится дальше конца то они меняются местами.
        :param start:
        :param end:
        :return:
        """
        if start > end:
            tmp = start
            start = end
            end = tmp
        self.chromosome = self.chromosome[:start] + self.chromosome[start:end][::-1] + self.chromosome[end:]

    def translocation_mutation(self, start_first, end_first, start_second, end_second):
        """
        Мутация-транслокация. Два выбранных промежутка меняются местами.
        Все указанные начала и концы отрезков будут отсортированы в возрастающем порядке дабы избежать наложения.
        :param start_first:
        :param end_first:
        :param start_second:
        :param end_second:
        :type start_first: int
        :type end_first: int
        :type start_second: int
        :type end_second: int
        :return:
        """
        arr = [start_first, end_first, start_second, end_second]  # сортировка во избежание наложения
        arr.sort()
        self.chromosome = self.chromosome[:arr[0]] + self.chromosome[arr[0]:arr[1]] + self.chromosome[arr[1]:arr[2]] + \
                          self.chromosome[arr[2]:arr[3]] + self.chromosome[arr[3]:]

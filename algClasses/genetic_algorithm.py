import math
import random
import copy

from algClasses.chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, population_count, src, operator, probability=0):
        """
        Создание простого генетического алгоритма.
        :param population_count: количество особей в популяции
        :param src: путь до файла с тасками
        :param operator: массив с номерами используемых операторов
        :param probability: вероятность мутации. Используется только в обычной бинарной мутации
        :type population_count: int
        :type src: str
        :type operator: list
        """
        self.probability = probability
        if self.probability == 0:
            self.probability = random.random()
        # Структура массива operators: 0.выбор родителей, 1.скрещивание, 2.мутация, 3. формирование новой популяции
        self.operators = operator
        self.population = self.create_population(population_count, src)
        self.bestChromosome = None
        self.find_best_person()

    @staticmethod
    def create_population(population_count, src):
        """
        Создает новую популяцию.
        :param population_count: число особей в популяции
        :param src: путь до файла с популяцией
        :type population_count: int
        :type src: str
        :return: новая популяция
        :rtype: list
        """
        arr = []
        Chromosome.create_task_list(src)
        for i in range(population_count):
            arr.append(Chromosome)
        return arr

    def find_best_person(self):
        tmp_arr = self.population[:]
        tmp_arr.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        self.bestChromosome = copy.deepcopy(tmp_arr[0])

    # ----------------
    # Операторы выбора родителей
    # -----------------

    def panmixia(self):
        """
        Возвращает 2 случайные хромосомы
        :return: массив из двух случайных хромосом
        :rtype: list
        """
        return random.choices(self.population, k=2)

    def outbreeding(self):
        """
        Аутбридинг. Выбирает первую хромосому случайно, вторую подбирает из популяции по наибольшему Хемминговому расстоянию
        :return: массив из двух хромосом
        :rtype: list
        """
        hamming_array = []
        best_hamming = 0
        first_parent = random.choice(self.population)
        for chromosome in self.population:
            tmp_hamming = first_parent.hamming_distance(chromosome)
            if tmp_hamming == best_hamming:
                hamming_array.append(chromosome)
            if tmp_hamming > best_hamming:
                best_hamming = tmp_hamming
                hamming_array.clear()
                hamming_array.append(chromosome)
        return [first_parent, random.choice(hamming_array)]

    def selection(self):
        """
        Селекция. Возвращает две хромосомы у которых приспособленность не меньше чем средняя
        :return: массив из двух хромосом
        :rtype: list
        """
        avg_fit = 0
        for chromosome in self.population:
            avg_fit += chromosome.fit
        avg_fit = avg_fit / len(self.population)

        tmp_population = self.population[:]
        for chromosome in self.population:
            if chromosome.fit < avg_fit:
                tmp_population.remove(chromosome)
        return random.choices(tmp_population, k=2)

    # -------------------------------------------------------------
    # операторы создания новой популяции
    # -------------------------------------------------------------

    def substitution(self, new_population):
        """
        Полное замещение потомков родителями.
        :param new_population: Новая популяция хромосом
        :type new_population: list
        :return:
        """
        self.population = new_population

    def truncation(self, new_population, max_count_population):
        """
        Замещение. Из популяции родителей и потомков собирает новую популяцию, состоящую из лучших.
        :param new_population: Популяция потомков.
        :param max_count_population: Число особей в новом поколении.
        :type new_population: list
        :type max_count_population: int
        :return:
        """
        tmp_population = self.population + new_population
        tmp_population.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        tmp_population = tmp_population[:max_count_population - 1]
        self.population = tmp_population

    def elite_selection(self, new_population, max_count_population):
        """
        Элитарный отбор. Выбирается 10% лучших. Остальное замещается новыми потомками.
        :param new_population: Популяция потомков.
        :param max_count_population: Число особей в новом поколении.
        :type new_population: list
        :type max_count_population: int
        :return:
        """
        tmp_population = self.population + new_population
        tmp_population.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        tmp_population = tmp_population[:round(max_count_population * 0.1)]
        for i in range(max_count_population - len(tmp_population)):
            tmp_population.append(Chromosome())
        self.population = tmp_population

    def one_cycle(self):  # todo переписать на что-нибудь более приятное
        """
        Создает новое поколение хромосом основываясь на выбранных операторах и существующем поколении родителей.
        :return:
        """
        new_population = []
        for i in range(len(self.population) // 2):
            # выбор родителей
            if self.operators[0] == 0:
                parents = self.panmixia()
            elif self.operators[0] == 1:
                parents = self.outbreeding()
            else:
                parents = self.selection()

            # скрещивание
            if self.operators[1] == 0:
                children = parents[0].one_point_crossingover(parents[1],
                                                             random.randint(0, len(parents[1].chromosome) - 1))
            elif self.operators[1] == 1:
                children = parents[0].two_point_crossingover(parents[1],
                                                             random.randint(0, len(parents[1].chromosome) - 1),
                                                             random.randint(0, len(parents[1].chromosome) - 1))
            else:
                children = parents[0].binary_mask_crossingover(parents[1], random.choice(self.population))

            # мутация`
            if self.operators[2] == 0:
                children[0].common_binary_mutation(self.probability)
                children[1].common_binary_mutation(self.probability)
            elif self.operators[2] == 1:
                children[0].inversion_mutation(random.randint(0, len(self.population) - 1),
                                               random.randint(0, len(self.population) - 1))
                children[1].inversion_mutation(random.randint(0, len(self.population) - 1),
                                               random.randint(0, len(self.population) - 1))
            else:
                children[0].translocation_mutation(random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1))
                children[1].translocation_mutation(random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1),
                                                   random.randint(0, len(self.population) - 1))
            new_population.append(children[0])
            new_population.append(children[1])

            # отбор в новое поколение
            if self.operators[3] == 0:
                self.substitution(new_population)
            elif self.operators[3] == 1:
                self.truncation(new_population, len(self.population))
            else:
                self.elite_selection(new_population, len(self.population))
            self.find_best_person()

class CellGeneticAlgorithm(SimpleGeneticAlgorithm):
    def __init__(self, population_count, src, operator): # population_count должен быть квадратом числа
        super().__init__(population_count, src, operator)
        self.cells_population = []
        self.create_cells_population()

    def create_cells_population(self):
        col_row_count = round(math.sqrt(len(self.population)))
        # todo доделать
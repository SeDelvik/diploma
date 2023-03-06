import json
import math
import random
import copy

from algClasses.chromosome import Chromosome


class SimpleGeneticAlgorithm:
    def __init__(self, population_count: int, src: str, operator: list[int], probability=0):
        """
        Создание простого генетического алгоритма.
        :param population_count: Количество особей в популяции.
        :param src: Путь до файла с тасками.
        :param operator: Массив с номерами используемых операторовю
        :param probability: Вероятность мутации. Используется только в обычной бинарной мутации.
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
    def create_population(population_count: int, src: str) -> list[Chromosome]:
        """
        Создает новую популяцию.
        :param population_count: Число особей в популяции.
        :param src: Путь до файла с популяцией.
        :return: Новая популяция.
        """
        arr = []
        Chromosome.create_task_list(src)
        for i in range(population_count):
            chromosome = Chromosome()
            arr.append(chromosome)
        return arr

    def find_best_person(self):
        """
        Ищет лучшую особь в популяции и записывает в параметры экземпляра.
        :return:
        """
        tmp_arr = self.population[:]
        tmp_arr.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        self.bestChromosome = copy.deepcopy(tmp_arr[0])

    # ----------------
    # Операторы выбора родителей
    # -----------------

    def panmixia(self) -> list[Chromosome]:
        """
        Возвращает 2 случайные хромосомы.
        :return: Массив из двух случайных хромосом.
        """
        return random.choices(self.population, k=2)

    def outbreeding(self) -> list[Chromosome]:
        """
        Аутбридинг. Выбирает первую хромосому случайно, вторую подбирает из популяции по наибольшему
        Хемминговому расстоянию.
        :return: Массив из двух хромосом.
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

    def selection(self) -> list[Chromosome]:
        """
        Селекция. Возвращает две хромосомы у которых приспособленность не меньше чем средняя
        :return: массив из двух хромосом
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

    def substitution(self, new_population: list[Chromosome]):
        """
        Полное замещение потомков родителями.
        :param new_population: Новая популяция хромосом
        :return:
        """
        self.population = new_population

    def truncation(self, new_population: list[Chromosome], max_count_population: int):
        """
        Замещение. Из популяции родителей и потомков собирает новую популяцию, состоящую из лучших.
        :param new_population: Популяция потомков.
        :param max_count_population: Число особей в новом поколении.
        :return:
        """
        tmp_population = self.population + new_population
        tmp_population.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        tmp_population = tmp_population[:max_count_population - 1]
        self.population = tmp_population

    def elite_selection(self, new_population: list[Chromosome], max_count_population: int):
        """
        Элитарный отбор. Выбирается 10% лучших. Остальное замещается новыми потомками.
        :param new_population: Популяция потомков.
        :param max_count_population: Число особей в новом поколении.
        :return:
        """
        tmp_population = self.population + new_population
        tmp_population.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        tmp_population = tmp_population[:round(max_count_population * 0.1)]
        for i in range(max_count_population - len(tmp_population)):
            tmp_population.append(Chromosome())
        self.population = tmp_population

    def one_cycle(self):
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
    def __init__(self, population_count, src, operator):  # population_count должен быть квадратом числа
        super().__init__(population_count, src, operator)  # здесь нужно всего 2 оператора
        self.cells_population = []
        self.create_cells_population()

    def create_cells_population(self):
        """
        Создает новую ячеистую популяцию на базе внутреннего списка особей
        :return:
        """
        array = []
        col_row_count = round(math.sqrt(len(self.population)))
        pos = 0
        for i in range(col_row_count):
            new_row = []
            array.append(new_row)
            for j in range(col_row_count):
                new_row.append(self.population[pos])
                pos += 1
        self.cells_population = array

    def get_partner_for_cell(self, row: int, col: int) -> list[Chromosome]:
        """
        Возвращает список из 4 соседей хромосомы, указанной по номеру строки и колонки.
        :param row: Номер строки (начинается с 0).
        :param col: Номер колонки (начинается с 0).
        :return: Массив из 4 хромосом.
        """
        col_row_count = round(math.sqrt(len(self.population)))
        maybe_partners = []
        if row == 0:
            maybe_partners.append(self.cells_population[col_row_count - 1][col])  # верх
            maybe_partners.append(self.cells_population[row + 1][col])  # низ
        elif row == col_row_count - 1:
            maybe_partners.append(self.cells_population[row - 1][col])  # верх
            maybe_partners.append(self.cells_population[0][col])  # низ
        else:
            maybe_partners.append(self.cells_population[row - 1][col])  # верх
            maybe_partners.append(self.cells_population[row + 1][col])  # низ

        if col == 0:
            maybe_partners.append(self.cells_population[row][col_row_count - 1])  # лево
            maybe_partners.append(self.cells_population[row][col + 1])  # право
        elif col == col_row_count - 1:
            maybe_partners.append(self.cells_population[row][col - 1])  # лево
            maybe_partners.append(self.cells_population[row][0])  # право
        else:
            maybe_partners.append(self.cells_population[row][col - 1])  # лево
            maybe_partners.append(self.cells_population[row][col + 1])  # право

        return maybe_partners

    def new_selection(self, row: int, col: int) -> list[Chromosome]:
        """
        Селекция для ячеистого генетического алгоритма. Создает пару из двух родителей.
        :param row: Номер строки (начинается с 0).
        :param col: Номер колонки (начинается с 0).
        :return: Массив из двух хромосом-родителей.
        """
        parent1 = self.cells_population[row][col]
        parents_array = self.get_partner_for_cell(row, col)
        parents_array.sort(key=lambda chromosome: chromosome.fit, reverse=True)
        parent2 = parents_array[0]
        return [parent1, parent2]

    def one_cycle(self):
        """
        Один цикл работы ячеистого генетического алгоритма. После работы поколение заменяется на новое.
        :return:
        """
        col_row_count = round(math.sqrt(len(self.population)))
        new_flat_population = []
        for i in range(col_row_count):
            for j in range(col_row_count):
                # выбор родителей
                parents = self.new_selection(i, j)
                # скрещивание
                if self.operators[0] == 0:
                    children = parents[0].one_point_crossingover(parents[1],
                                                                 random.randint(0, len(parents[1].chromosome) - 1))
                elif self.operators[0] == 1:
                    children = parents[0].two_point_crossingover(parents[1],
                                                                 random.randint(0, len(parents[1].chromosome) - 1),
                                                                 random.randint(0, len(parents[1].chromosome) - 1))
                else:
                    children = parents[0].binary_mask_crossingover(parents[1], random.choice(self.population))

                # мутация
                if self.operators[1] == 0:
                    children[0].common_binary_mutation(self.probability)
                    children[1].common_binary_mutation(self.probability)
                elif self.operators[1] == 1:
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
                children.sort(key=lambda chromosome: chromosome.fit, reverse=True)
                new_flat_population.append(children[0])
        self.population = new_flat_population
        self.find_best_person()
        self.create_cells_population()


class IslandGeneticAlgorithm:
    def __init__(self, count_island: int, one_island_population_count: int, src_doc: str, count_generation: int,
                 count_person_in_swap: int):
        """
        Создает новый Островной генетический алгоритм.
        :param count_island: Количество островов.
        :param one_island_population_count: Величина популяции на каждом острове.
        :param src_doc: Путь до файла с тасками.
        :param count_generation: Количество поколений до обмена между островами.
        :param count_person_in_swap: Количество особей для обмена между островами.
        """
        self.count_generation = count_generation
        self.count_person_in_swap = count_person_in_swap
        self.islands = []
        self.create_islands(count_island, one_island_population_count, src_doc)

    def create_islands(self, count_islands: int, one_islands_population_count: int, src_doc: str):
        """
        Создает \"острова\".
        :param count_islands: Количество островов.
        :param one_islands_population_count: Количество особей на одном острове.
        :param src_doc: Файл с тасками.
        :return:
        """
        for i in range(count_islands):
            simple_gen_alg = SimpleGeneticAlgorithm(one_islands_population_count, src_doc,
                                                    [random.randint(0, 3), random.randint(0, 3), random.randint(0, 3),
                                                     random.randint(0, 3)])
            self.islands.append(simple_gen_alg)

    def one_cycle(self):
        """
        Производит один цикл островного генетического алгоритма.
        :return:
        """
        for i in range(self.count_generation):  # прокручивает циклы смены поколений на всех островах
            for island in self.islands:
                island.one_cycle()
        arr_bests = []  # создание массива в котором будут храниться временные лучшие особи для обмена
        for island in self.islands:
            island.population.sort(key=lambda chromosome: chromosome.fit, reverse=True)  # сортирует все популяции островов по приспособленности.
            best_people = []
            for i in range(self.count_person_in_swap):
                best_people.append(island.population.pop(0))  # вынимает лучших из другой популяции
            arr_bests.append(best_people)  # и сохраняет во временный массив
        for i in range(len(self.islands)):  # обменивает популяции со следующим
            if i == len(self.islands)-1:
                self.islands[i].population = self.islands[i].population + arr_bests[0]
            self.islands[i].population = self.islands[i].population + arr_bests[i+1]

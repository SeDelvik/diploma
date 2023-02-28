from algClasses.chromosome import Chromosome


class Simple_GA:
    def __init__(self, population_count, src):
        self.population = self.create_population(population_count, src)
        self.bestChromosome = None

    def create_population(self, population_count, src):
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
        Chromosome(src)
        for i in range(population_count):
            arr.append(Chromosome)
        return arr

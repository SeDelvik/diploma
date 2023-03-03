from algClasses.chromosome import Chromosome
from algClasses.genetic_algorithm import SimpleGeneticAlgorithm


def main():
    Chromosome.create_task_list('./res/testTaskList.json')
    chrom = Chromosome()
    for tsk in chrom.task_list:
        print(tsk)

    chrom2 = Chromosome()
    print(f"self: {chrom}")
    print(f"parent2: {chrom2}")

    for obj in chrom.one_point_crossingover(chrom2, 2):
        print(f"children: {obj}")

    SimpleGeneticAlgorithm(10, './res/testTaskList.json', [0, 0, 0, 0])


if __name__ == '__main__':
    main()

from algClasses.chromosome import Chromosome
from algClasses.genetic_algorithm import Simple_GA


def main():
    chrom = Chromosome('./res/testTaskList.json')
    for tsk in chrom.task_list:
        print(tsk)

    chrom2 = Chromosome()
    print(f"parent1: {chrom}")
    print(f"parent2: {chrom2}")

    for obj in chrom.one_point_crossingover(chrom2, 2):
        print(f"children: {obj}")

    Simple_GA(10, './res/testTaskList.json')


if __name__ == '__main__':
    main()

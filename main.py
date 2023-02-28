import json
#import algClasses.chromosome as chromosome
from algClasses.chromosome import Chromosome
from algClasses.task import Task
import algClasses.chromosome as chromLib


def main():
    # f = open('./res/testRes.json')
    # text = f.read()
    # tmp = json.loads(text)
    with open('./res/testRes.json') as fp:
        tmp = json.load(fp)
        print(tmp[1]["bar"])
    chrom = Chromosome('./res/testTaskList.json')
    for tsk in chrom.task_list:
        print(tsk)

    chrom2 = Chromosome()
    print(f"parent1: {chrom}")
    print(f"parent2: {chrom2}")

    for obj in chromLib.one_point_croossingover(chrom,chrom2,2):
        print(f"children: {obj}")


if __name__ == '__main__':
    main()

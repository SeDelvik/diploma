import json
import algClasses.chromosome as chromosome
import algClasses.task as task


def main():
    # f = open('./res/testRes.json')
    # text = f.read()
    # tmp = json.loads(text)
    with open('./res/testRes.json') as fp:
        tmp = json.load(fp)
        print(tmp[1]["bar"])
    chrom = chromosome.Chromosome('./res/testTaskList.json')
    print(chrom.task_list)


if __name__ == '__main__':
    main()

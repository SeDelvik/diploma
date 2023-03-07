import unittest
from algClasses.chromosome import Chromosome


class TestChromosome(unittest.TestCase):
    def setUp(self) -> None:
        Chromosome.create_task_list("./res/testTaskList.json")
        self.chromosome_one = Chromosome()
        self.chromosome_two = Chromosome()

    def test_one_point_crossingover(self):
        self.chromosome_one.chromosome = [0, 0, 0, 0, 0]
        self.chromosome_two.chromosome = [1, 1, 1, 1, 1]
        children = self.chromosome_one.one_point_crossingover(self.chromosome_two, 3)
        self.assertTrue(assert_list(children[0].chromosome, [0, 0, 0, 1, 1]))
        self.assertTrue(assert_list(children[1].chromosome, [1, 1, 1, 0, 0]))

    def test_two_point_crossingover(self):
        self.chromosome_one.chromosome = [0, 0, 0, 0, 0]
        self.chromosome_two.chromosome = [1, 1, 1, 1, 1]
        children = self.chromosome_one.two_point_crossingover(self.chromosome_two, 3, 2)
        self.assertTrue(assert_list(children[0].chromosome, [0, 0, 1, 0, 0]))
        self.assertTrue(assert_list(children[1].chromosome, [1, 1, 0, 1, 1]))

    def test_binary_mask_crossingover(self):
        binary_mask = Chromosome()
        binary_mask.chromosome = [1, 1, 1, 0, 0]
        self.chromosome_one.chromosome = [0, 0, 0, 0, 0]
        self.chromosome_two.chromosome = [1, 1, 1, 1, 1]
        children = self.chromosome_one.binary_mask_crossingover(self.chromosome_two, binary_mask)
        self.assertTrue(assert_list(children[0].chromosome, [0, 0, 0, 1, 1]))
        self.assertTrue(assert_list(children[1].chromosome, [1, 1, 1, 0, 0]))

    def test_inversion_mutation(self):
        self.chromosome_one.chromosome = [0, 0, 0, 1, 1]
        self.chromosome_one.inversion_mutation(1, 4)
        self.assertTrue(assert_list(self.chromosome_one.chromosome, [0, 1, 0, 0, 1]))

    def test_translocation_mutation(self):
        self.chromosome_one.chromosome = [0, 0, 0, 1, 1]
        self.chromosome_one.translocation_mutation(1, 3, 2, 4)
        self.assertTrue(assert_list(self.chromosome_one.chromosome, [0, 1, 0, 0, 1]))


def assert_list(arr1: list[int], arr2: list[int]) -> bool:
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            print(f"arr1: {arr1}\narr2: {arr2}")
            return False
    return True

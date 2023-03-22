import json


class Task:

    def __init__(self, time: int, cost: int, deadline: int, name=""):
        """Хранит данные о задаче"""
        self.name = name
        self.time = time
        self.cost = cost
        self.deadline = deadline

    def __str__(self):
        return f"name: {self.name}, time: {self.time}, cost: {self.cost}, deadline:{self.deadline}"

    def to_JSON(self):
        return self.__dict__

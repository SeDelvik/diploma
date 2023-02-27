class Task:
    """Хранит данные о задаче"""

    def __init__(self, time, cost, deadline, name=""):
        self.name = name
        self.time = time
        self.cost = cost
        self.deadline = deadline

    def __str__(self):
        return f"name: {self.name}, time: {self.time}, cost: {self.cost}, deadline:{self.deadline}"

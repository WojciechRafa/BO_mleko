import data
import struct

from typing import List
from typing import Tuple


def profits_calc(solution: List):
    profits_sum = 0
    for day in solution:
        for node_and_milk in day:
            node, milk = node_and_milk
            profits_sum += milk * node.data[3]
    return profits_sum


def drive_cost(solution: List):
    sum = 0
    for day in solution:
        day_copy = day[:]
        day_copy.append((data.b, 0))
        for i in range(len(day_copy) - 1):
            sum += data.G.get_lenght(day_copy[i][0], day_copy[i + 1][0])
    return sum


def cooling_cost(solution: List):
    sum = 0
    for day in solution:
        cooled_milk = 0
        for node_and_milk in day:
            node, milk = node_and_milk
            if node.name == 'r':
                cooled_milk += milk
            elif node.name == 'm':
                cooled_milk -= milk
            elif node.name == 'b':
                if milk > 0:# jeżeli mleko > 0 w bazie to oznacza, że mleko jest zabierane z bazy
                    cooled_milk += milk
            else:
                raise RuntimeError("Nieprawidłowy typ nod-a")

        sum += cooled_milk * data.cs
    return sum


def t_fun(solution):
    profit = profits_calc(solution)
    d_cost = drive_cost(solution, data.G)
    cool_cost = cooling_cost(solution)

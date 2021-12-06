import data
import struct
import limits

from typing import List
from typing import Tuple


def profits_calc(solution: List) -> int:
    profits_sum = 0
    for day in solution:
        for node_and_milk in day:
            node, milk = node_and_milk
            profits_sum += milk * node.data[3]
    return profits_sum


def drive_cost(solution: List) -> float:
    sum = 0
    for day in solution:
        day_copy = day[:]
        day_copy.append((data.b, 0))
        for i in range(len(day_copy) - 1):
            sum += data.G.get_lenght(day_copy[i][0], day_copy[i + 1][0])*data.cp
    return sum


def cooling_cost(solution: List) -> float:
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


def t_fun(solution) ->Tuple[float, bool]:
    profit = profits_calc(solution)
    d_cost = drive_cost(solution)
    cool_cost = cooling_cost(solution)

    old_milk_pen, old_milk_bool = limits.check_r_time(solution)
    dist_pen, dist_bool = limits.check_distance(solution)
    volume_pen, volume_bool = limits.check_milk_volume(solution)
    mlecz_pen = limits.mlecz_penalties(solution)

    pen_sum = old_milk_pen*data.old_milk_error_cost+dist_pen*data.dist_error_cost+volume_pen*data.volume_error_cost+mlecz_pen;
    is_legal = old_milk_bool is True and dist_bool is True and volume_bool is True

    fun_value = profit - d_cost - cool_cost - pen_sum

    return fun_value, is_legal




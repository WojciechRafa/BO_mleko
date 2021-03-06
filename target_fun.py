import data
import d_struct
import limits

from typing import List
from typing import Tuple

# Oblicza zysk ze sprzedaży mleka
def profits_calc(solution: List) -> int:
    profits_sum = 0
    for i in range(len(data.SM)):
        milk_sum = 0
        for day in solution:
            for node_and_milk in day:
                node, milk = node_and_milk
                if (node.name == 'm') and (node.nr == i):
                    milk_sum += milk
        profits_sum += milk_sum * data.SM[i][3]
    return profits_sum

# Oblicza koszt przejazdu
def drive_cost(solution: List) -> float:
    sum = 0
    for day in solution:
        day_copy = day[:]
        day_copy.append((data.b, 0))
        for i in range(len(day_copy) - 1):
            sum += data.G.get_lenght(day_copy[i][0], day_copy[i + 1][0])*data.cp
    return sum

# Oblicza koszt schładzania mleka
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

# Funkcja celu. Oblicza całkowity zysk/stratę oraz sprawdza, czy rozwiązanie jest dopuszczalne
def t_fun(solution: [List[List[List]]]) ->Tuple[float, bool]:
    profit = profits_calc(solution)
    d_cost = drive_cost(solution)
    cool_cost = cooling_cost(solution)

    old_milk_pen, old_milk_bool = limits.check_r_time(solution)
    dist_cost, dist_pen, dist_bool = limits.check_distance(solution)
    milk_volume_cost, volume_pen, volume_bool = limits.check_milk_volume(solution)
    mlecz_pen = limits.mlecz_penalties(solution)
    cost_errors_schedule, is_shedule_ok = limits.check_schedule(solution)
    cost_r_milk_volume, is_ok_r_milk_volume = limits.check_r_milk_volume(solution)
    #cost_origin, is_ok_origin = limits.check_milk_orgin(solution)


    pen_sum = old_milk_pen*data.old_milk_error_cost+dist_pen*data.dist_error_cost+volume_pen*data.volume_error_cost+mlecz_pen+cost_errors_schedule#+cost_r_milk_volume
    is_legal = old_milk_bool and dist_bool and volume_bool and is_shedule_ok and is_ok_r_milk_volume #and is_ok_origin

    fun_value = profit - d_cost - cool_cost - pen_sum - milk_volume_cost - dist_cost #- cost_origin
    return fun_value, is_legal



from typing import Tuple
from typing import List

import d_struct
import data


#sprawdza jak dawno mleko było odbierane od rolnika
def check_r_time(solution) -> Tuple[int, bool]:
    numbers_of_errors: int = 0
    is_check_r_time_ok: bool = True
    for i in range(len(data.SR)):
        sum_milk = 0 
        nr_day = 0
        for day in solution:
            nr_day += 1
            for node_and_milk in day:
                node, milk = node_and_milk
                if (node.name == 'r') and (node.nr == i):
                    sum_milk += milk
            if nr_day == 3:
                nr_day = 0
                if sum_milk != (data.SR[i][0]*3):
                    numbers_of_errors += 1
                sum_milk = 0
    if numbers_of_errors > 0:
        is_check_r_time_ok = False

    return numbers_of_errors, is_check_r_time_ok > 0


#sprawdza, czy trasa nie jest za długa
def check_distance(solution: List) -> Tuple[int, int, bool]:
    numbers_of_errors: int = 0
    is_day_dist_ok: bool = True

    volume = 0
    for dzien in solution:
        distance = 0
        lista_krokow = []
        for krok in dzien:
            lista_krokow.append(krok[0])
        lista_krokow.append(d_struct.Node("b"))
        for i in range(len(lista_krokow) - 1):
            distance += data.G.get_lenght(lista_krokow[i], lista_krokow[i+1])
        if distance > data.lk:
            numbers_of_errors += 1
            volume += distance - data.lk

    if numbers_of_errors > 0:
        is_day_dist_ok = False

    return volume*data.dist_cost, numbers_of_errors, is_day_dist_ok


#sprawdza, czy nie przekroczono pojemności cysterny
def check_milk_volume(solution: List) -> Tuple[int, int, bool]:
    numbers_of_errors: int = 0
    volume = 0
    for day in solution:
        milk_quantity = 0
        for node_and_milk in day:
            node, milk = node_and_milk
            if node.name == 'r':
                milk_quantity += milk
            elif node.name == 'm':
                milk_quantity -= milk
            elif node.name == 'b':
                milk_quantity += milk
            else:
                raise RuntimeError("Nieprawidłowy typ nod-a")

            if milk_quantity > data.mc or milk_quantity < 0:
                numbers_of_errors += 1
                volume = volume + ((milk_quantity-data.mc)*10)
    if numbers_of_errors > 0:
        return volume, numbers_of_errors, False
    else:
        return volume, numbers_of_errors, True


#oblicza kary umowne z mleczarni
def mlecz_penalties(solution: List) -> int:
    sum_penalty = 0
    for i in range(len(data.SM)):
        milk_sum = 0
        for day in solution:
            for node_and_milk in day:
                node, milk = node_and_milk
                if (node.name == 'm') and (node.nr == i):
                    milk_sum += milk
        if milk_sum < data.SM[i][1]:
            sum_penalty += 10 * (data.SM[i][1]-milk_sum)
        if milk_sum > data.SM[i][2]:
            sum_penalty += 10 * (milk_sum - data.SM[i][1])
    return sum_penalty


#sprawdza, czy mleko jest dostarczane do mleczarnii zgodnie z harmonogramem
def check_schedule(solution: List) -> Tuple[int, bool]:
    cost: int = 0
    is_shedule_ok: bool = True
    d: int = 0
    for day in solution:
        d += 1
        for node_milk in day:
            node, milk = node_milk
            if node.name =='m':
                if not d in node.data[0]:
                    cost += node.data[4]
    if cost > 0:
        is_shedule_ok = False
    return cost, is_shedule_ok


#sprawdzanie, czy nie odbieramy więcej mleka, niż rolnik jest w stanie wyprodukować
def check_r_milk_volume(solution: List) -> Tuple[int, bool]:
    cost = 0
    is_ok = True

    for nr_day, day in enumerate(solution):
        for nr_node, node_milk in enumerate(day):
            node, milk = node_milk
            if node.name == 'r':
                milk_at_farmer = data.how_much_milk_is_in_point(solution, nr_day, nr_node)
                if milk > milk_at_farmer:
                    cost += 500 + ((milk-milk_at_farmer)*10)
    if cost > 0:
        is_ok = False                
    return cost, is_ok

def check_milk_orgin(solution: List[List[List]]) -> Tuple[int, bool]:# sprawdzenie tego czy przepływ mleka ma sens
    penalty = 0
    is_ok = True
    for day in solution:
        milk_in_day = 0
        for node in day:
            if node[0].name == 'm':
                milk_in_day -= node[1]
            else:
                milk_in_day += node[1]
            if milk_in_day < 0:
                is_ok = False
                penalty += data.orgin_stat_error + abs(milk_in_day)*data.origin_p_cost
    return penalty, is_ok
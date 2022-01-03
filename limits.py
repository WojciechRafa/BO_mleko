from typing import Tuple
from typing import List

import d_struct
import data


def check_r_time(solution) -> Tuple[int, bool]:
    old_milk = 0
    for day in solution:
        for node_and_milk in day:
            node, milk = node_and_milk
            if node.name == 'r':
                if node.data[2] > data.max_d:
                    old_milk += 1
    return old_milk, old_milk > 0


def check_distance(solution: List) -> Tuple[int, bool]:  # zwrca koszt przejechania dystansu oraz czy któregoś dnia przekroczono ograniczenie
    numbers_of_errors: int = 0
    is_day_dist_ok: bool = True
    for dzien in solution:
        distance = 0
        lista_krokow = []
        for krok in dzien:
            lista_krokow.append(krok[0])
        lista_krokow.append(d_struct.b)
        for i in range(len(lista_krokow) - 1):
            distance += data.G.get_lenght(lista_krokow[i], lista_krokow[i+1])
        if distance > data.lk:
            numbers_of_errors += 1

    if numbers_of_errors > 0:
        is_day_dist_ok = False

    return numbers_of_errors, is_day_dist_ok


def check_milk_volume(solution: List) -> Tuple[int, bool]:
    numbers_of_errors: int = 0
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
    if numbers_of_errors > 0:
        return numbers_of_errors, False
    else:
        return numbers_of_errors, True


def mlecz_penalties(solution: List) -> int:
    sum_penalty = 0
    for dairy in data.SM:
        if dairy[5] < dairy[1] or dairy[5] > dairy[2]:
            sum_penalty += dairy[4]
    return sum_penalty


def check_schedule(solution: List) -> Tuple[int, bool]:
    numbers_of_errors: int = 0
    is_shedule_ok: bool = True
    d: int = 0
    for day in solution:
        d += 1
        milk_quantity = 0
        for node_milk in day:
            node, milk = node_milk
            if node.nama =='m':
                if not d in node.data[0]:
                    numbers_of_errors += 1
    if numbers_of_errors > 0:
        is_shedule_ok = False
    return numbers_of_errors, is_shedule_ok

from typing import Tuple
from typing import List

import struct
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


def check_distance(lk_, cp_, R_) -> Tuple[
    float, bool]:  # zwrca koszt przejechania dystansu oraz czy któregoś dnioa przekroczono ograniczenie
    p_km: float = 0
    is_day_dist_ok: bool = True
    for dzien in R_:
        distance = 0
        lista_krokow = struct.b
        for krok in dzien:
            lista_krokow.append(krok[0])
        lista_krokow.append(struct.b)

        for i in range(len(lista_krokow) - 1):
            distance = distance + connection[struct.G.get_node_idx(lista_krokow[i])][
                struct.G.get_node_idx(lista_krokow[i + 1])]

            if distance > lk_:
                is_day_dist_ok = False
            else:
                p_km = p_km + distance * cp_

    return p_km, is_day_dist_ok


def mlecz_penalties(solution: List) -> int:
    sum_penalty = 0
    for dairy in data.SM:
        if dairy[5] < dairy[1] or dairy[5] > dairy[2]:
            sum_penalty += dairy[4]
    return sum_penalty

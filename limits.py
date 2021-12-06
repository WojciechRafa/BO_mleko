from typing import Tuple


def check_r_time(max_d, SR_):
    k = 0
    for rolnik in SR_.keys():
        if ((SR_[rolnik][2]) > max_d):
            k = k +(SR_[rolnik][1]*SR_[rolnik][3])
    return k


def check_distance(lk_, cp_, R_) -> Tuple[float, bool]:  # zwrca koszt przejechania dystansu oraz czy któregoś dnioa przekroczono ograniczenie
    p_km: float = 0
    is_day_dist_ok: bool = True
    for dzien in R_:
        distance = 0
        lista_krokow = [Node("b")]
        for krok in dzien:
            lista_krokow.append(krok[0])
        lista_krokow.append(Node("b"))

        for i in range(len(lista_krokow) - 1):
            distance = distance + connection[G.get_node_idx(lista_krokow[i])][G.get_node_idx(lista_krokow[i + 1])]

            if distance > lk_:
                is_day_dist_ok = False
            else:
                p_km = p_km + distance * cp_

    return p_km, is_day_dist_ok

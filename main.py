from typing import List
from typing import Tuple
import matplotlib.pyplot as plt

import data
import d_struct
import steps
import target_fun
import limits

#główne parametry algorytmu
max_iter = 50 #maksymalna ilość iteracji
n = 5 #liczba sprawdzanych kroków w jednej iteracji
TL_dl = 3 #długość listy tabu
#pomocnicze listy do badania przebiegu algorytmu
values = [] #lista przechowująca kolejne wartości funkcji celu
is_acceptable = []#lista przechowująca kolejne informacje o wykonywalniści funkcji

lr = 5 # liczba rolników
min_r_m = 20 # minimalna dzienna liczba produkowanych litrów mleka w gospodarstwie
max_r_m = 200 # maksymalna dzienna liczba produkowanych litrów mleka w gospodarstwie

lm = 3 # liczba mleczarnii
min_m_m = (100, 300) # zakres dla minimalnej ilości przyjmowanych litrów mleka
max_m_m = (500, 800) # zakres dla maksymalnej ilości przyjmowanych litrów mleka
c_range = (1, 5) # zakres cen za litr
k_range = (100, 500) # zakres kar umownych

l_ele = lr + lm + 1 #liczba węzłów grafu
con_range = (1, 10) #zakres połączeń między wierzchołkami


if __name__ == '__main__':
    SM, SR, connection, start_solution, r, m, b, node_list, G = data.create_data(lr, min_r_m, max_r_m, lm, min_m_m, max_m_m, c_range, k_range, l_ele, con_range)
    data.SM = SM
    data.SR = SR
    data.connection = connection
    data.start_solution = start_solution
    data.r = r
    data.m = m
    data.b = b
    data.node_list = node_list
    data.G = G



    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution #początkowe rozwiązanie losowe

    # tymczasowow zakomneotwane
    max_iter = int(input("Podaj liczbę iteracji: "))
    n = int(input("Podaj liczbę kroków sprawdzanych w jednej iteracji: "))
    TL_dl = int(input("Podaj długość listy tabu: "))


    result = steps.get_random_steps(R, 5)
    print(result)



    iter = 0
    TL = []
    made_move = 0
    #pierwszy obieg algorytmu
    fun_value, is_legal = target_fun.t_fun(R)

    the_best_result = float('inf')

    while iter < max_iter:
        #generowanie nowych rozwiązań i wybór najlepszego
        steps_list = steps.get_random_steps(R, n)

        score = []
        result_list = []
        s_list = []
        is_accpet = []

        for step in steps_list:
            changed_ttable = steps.make_step(steps.make_timetable_copy(R), step)
            new_fun_value, is_legal = target_fun.t_fun(changed_ttable)

            score.append(new_fun_value)
            result_list.append(changed_ttable)
            s_list.append(step)
            is_accpet.append(is_legal)

        while len(score) > 0:
            max_el = max(score)
            max_el_idx = score.index(max_el)
            the_best_step = s_list[max_el_idx]

            if the_best_step not in TL:
                values.append(max_el)
                TL.append(s_list[max_el_idx])
                is_acceptable.append(is_accpet[max_el_idx])
                R = result_list[max_el_idx]
                break
            elif len(score) > 1:
                if max_el > the_best_result:
                    values.append(max_el)
                    TL.append(s_list[max_el_idx])
                    is_acceptable.append(is_accpet[max_el_idx])
                    R = result_list[max_el_idx]
                    break
                else:
                    del score[max_el_idx]
                    del result_list[max_el_idx]
                    del s_list[max_el_idx]
                    del is_accpet[max_el_idx]
            else:
                values.append(max_el)
                TL.append(s_list[max_el_idx])
                is_acceptable.append(is_accpet[max_el_idx])
                R = result_list[max_el_idx]
                break

        #obsługa listy tabu
        if len(TL) >= TL_dl:
            TL.remove(TL[0])

        iter += 1
    #wyświetlanie wyników
    nr = 0
    for day in R:
        nr += 1
        print('Dzień',nr)
        for w in day:
            print(w[0].name,w[0].nr,'->',w[1])
        print('\r')
    print('Zysk:', max(values))
    #wizualizacja przebiegu algorytmu
    plt.plot(values)
    plt.xlabel('iteracja')
    plt.ylabel('wartość')
    plt.show()



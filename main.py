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
    data.create_data(lr, min_r_m, max_r_m, lm, min_m_m, max_m_m, c_range, k_range, l_ele, con_range)
    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution #początkowe rozwiązanie losowe
    max_iter = int(input("Podaj liczbę iteracji: "))
    n = int(input("Podaj liczbę kroków sprawdzanych w jednej iteracji: "))
    TL_dl = int(input("Podaj długość listy tabu: "))

    result = steps.get_random_steps(R, 5)
    print(result)

    for step in result:
        changed_ttable = steps.make_step(steps.make_timetable_copy(R), step)
        for day in changed_ttable:
            print(day)
        print('\n\n')

    iter = 0
    TL = []
    made_move = 0
    #pierwszy obieg algorytmu 
    fun_value, is_legal = target_fun.t_fun(R)


    while iter < max_iter:
        #generowanie nowych rozwiązań i wybór najlepszego
        steps_list = steps.get_random_steps(R, n)
        for step in steps_list:
            if step not in TL:
                changed_ttable = steps.make_step(steps.make_timetable_copy(R), step)
                new_fun_value, is_legal = target_fun.t_fun(changed_ttable)
                if new_fun_value >= fun_value:
                    R = changed_ttable
                    fun_value = new_fun_value
                    made_move = step
        values.append(fun_value) 
    
        #obsługa listy tabu
        TL.append(made_move)
        if len(TL) >= TL_dl:
            TL.remove(TL[0])


    #wizualizacja wyników
    # plt.plot(values)
    # plt.xlabel('iteracja')
    # plt.ylabel('wartość')
    # plt.show()



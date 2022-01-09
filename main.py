from typing import List
from typing import Tuple

import data
import d_struct
import steps
import target_fun

#główne parametry algorytmu
max_iter = 50 #maksymalna ilość iteracji
n = 5 #liczba sprawdzanych kroków w jednej iteracji


if __name__ == '__main__':
    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution #początkowe rozwiązanie losowe

    # result = steps.get_random_steps(R, 5)
    # print(result)

iter = 0

#pierwszy obieg algorytmu 
fun_value, is_legal = target_fun.t_fun(R)


while iter < max_iter:
    #generowanie nowych rozwiązań i wybór najlepszego
    new_result = steps.get_random_steps(R, n)
    for ele in new_result:
        pass
    #obsługa listy tabu
    #wizualizacja wyników

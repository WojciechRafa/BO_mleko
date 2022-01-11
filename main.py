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

#pomocnicze listy do badania przebiegu algorytmu
values = [] #lista przechowująca kolejne wartości funkcji celu

if __name__ == '__main__':
    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution #początkowe rozwiązanie losowe

    result = steps.get_random_steps(R, 5)
    print(result)

    for step in result:
        changed_ttable = steps.make_step(steps.make_timetable_copy(R), step)
        for day in changed_ttable:
            print(day)
        print('\n\n')

iter = 0

#pierwszy obieg algorytmu 
# fun_value, is_legal = target_fun.t_fun(R)


# while iter < max_iter:
#     #generowanie nowych rozwiązań i wybór najlepszego
#     steps_list = steps.get_random_steps(R, n)
#     for ele in steps_list:
#         new_R = steps.make_step(R,ele)
#         new_fun_value, is_legal = target_fun.t_fun(new_R)
#         if new_fun_value >= fun_value:
#             R = new_R
#             fun_value = new_fun_value
#     values.append(fun_value) 
   
#     #obsługa listy tabu


#wizualizacja wyników
# plt.plot(values)
# plt.xlabel('iteracja')
# plt.ylabel('wartość')
# plt.show()



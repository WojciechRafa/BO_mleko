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


def start_alg(iter, max_step, tabu_l, iterator):
    # pomocnicze listy do badania przebiegu algorytmu
    values = []  # lista przechowująca kolejne wartości funkcji celu
    is_acceptable = []  # lista przechowująca kolejne informacje o wykonywalniści funkcji

    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution  # początkowe rozwiązanie losowe

    print('\r')
    
    # tymczasowow zakomneotwane
    #max_iter = int(input("Podaj liczbę iteracji: "))
    #n = int(input("Podaj liczbę kroków sprawdzanych w jednej iteracji: "))
    #TL_dl = int(input("Podaj długość listy tabu: "))

    max_iter = iter
    n = max_step
    TL_dl = tabu_l

    print('\r')

    result = steps.get_random_steps(R, 5)

    iter = 0
    TL = []
    made_move = 0
    # pierwszy obieg algorytmu
    fun_value, is_legal = target_fun.t_fun(R)

    the_best_result = 0
    all_solutions = []
    while iter < max_iter:
        # generowanie nowych rozwiązań i wybór najlepszego
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

        all_solutions.append(R)
        # obsługa listy tabu
        if len(TL) >= TL_dl:
            TL.remove(TL[0])

        iter += 1

    best_solution = []
    max_value = max(values)
    acceptable = False
    temp_max_value = float('inf') * -1

    for id, ele in enumerate(is_acceptable):
        if ele == True:
            if values[id] == max_value:
                best_solution = all_solutions[id]
                acceptable = True
                break
            elif values[id] > temp_max_value:
                temp_max_value = values[id]

    if best_solution == [] and True in is_acceptable:
        best_solution = all_solutions[values.index(temp_max_value)]
        max_value = temp_max_value
        acceptable = True

    elif best_solution == [] and not True in is_acceptable:
        best_solution = all_solutions[values.index(max_value)]
        acceptable = False
        print("Brak dopuszczalnych rozwiązań")
    
    print('\r')
    print("Najlepsze otrzymane rozwiązanie:")
    result:str = ""
    # wyświetlanie wyników
    nr = 0
    for day in best_solution:
        nr += 1
        print('Dzień', nr)
        result += 'Dzień ' + str(nr) + "\n"
        for w in day:
            print(w[0].name, w[0].nr, '->', w[1])
            result += str(w[0].name) + str(w[0].nr) + '->' + str(w[1]) + "\n"
        print('\r')
        result += "\r\n"
    print('Zysk:', max_value)
    result += "Zysk " + str(max_value) + "\n"
    if acceptable == True:
        print("Wynik jest dopuszczalny")
        result += "Wynik jest dopuszczalny"
    else:
        print("Wynik jest niedopuszczalny")
        result += "Wynik jest niedopuszczalny"

    text_file = open("Opis{}.txt".format(iterator), "w")
    text_file.write(result)
    text_file.close()

    # wizualizacja przebiegu algorytmu
    plt.plot(values)
    plt.xlabel('iteracja')
    plt.ylabel('wartość')
    #plt.show()
    plt.savefig('Fig{}.png'.format(iterator))


if __name__ == '__main__':
    #SM, SR, connection, start_solution, r, m, b, node_list, G = data.create_data(lr, min_r_m, max_r_m, lm, min_m_m, max_m_m, c_range, k_range, l_ele, con_range)

    data.SM = [
             # [(dni odbioru) 0 ,min 1, max 2, cena 3, kara umowan 4]
             [[3, 4], 139, 582, 4, 440],
             [[2, 2, 1], 130, 665, 3, 191],
             [[5], 167, 615, 4, 412]
         ]

    data.SR = [[25], [72], [97], [27], [126]]
    data.connection = [[0, 5, 5, 9, 4, 3, 2, 5, 4],
                       [5, 0, 7, 5, 5, 4, 3, 3, 6],
                       [5, 7, 0, 6, 5, 4, 3, 8, 7],
                       [9, 5, 6, 0, 9, 3, 7, 3, 5],
                       [4, 5, 5, 9, 0, 6, 3, 9, 5],
                       [3, 4, 4, 3, 6, 0, 4, 1, 3],
                       [2, 3, 3, 7, 3, 4, 0, 2, 6],
                       [5, 3, 8, 3, 9, 1, 2, 0, 1],
                       [4, 6, 7, 5, 5, 3, 6, 1, 0]]


    r = []
    r_size = len(data.SR)
    for i in range(r_size):
        r.append(d_struct.Node("r", i))
        r[i].data = data.SR[i]


    m = []
    m_size = len(data.SM)
    for i in range(m_size):
        m.append(d_struct.Node("m", i))
        m[i].data = data.SM[i]
    data.r = r
    data.m = m

    b = d_struct.Node("b")
    data.b = b
    node_list = [b] + r + m
    data.node_list = node_list
    G = d_struct.Neigbour_matrix()
    G.set_node_list(node_list)
    G.set_connection(data.connection)
    data.G = G

    data.start_solution =  [[[b, 0], [r[0], 30 ], [r[1], 50 ],  [m[1], 50 ],  [r[2], 60 ]],
                            [[b, 0], [r[1], 100], [r[0], 100],  [m[1], 160],  [m[0], 40 ]],
                            [[b, 0], [r[0], 30 ], [r[1], 50 ],  [r[2], 100],  [m[0], 180]],
                            [[b, 0], [r[0], 30 ], [r[2], 50 ],  [m[0], 50 ],  [r[2], 60 ]],
                            [[b, 0], [r[1], 100], [r[0], 100],  [m[1], 160],  [m[0], 40 ]]]

    tested = [50, 10, 20]

    #while True:
       # in_str = input("Rozpocząć algorytm [T] - Tak: ")
    for i in range(5):
        start_alg(tested[0], tested[1], tested[2], i)





import d_struct
from typing import List
from typing import Tuple
import random
import numpy as np

# Główne dane:
lk = 20  # limit kilonmetrów
pc = 200  # pojemność cysterny
cp = 0.1  # cena przejazdu jednego kilonmetra
cs = 0.2  # cena schłodzenia jednego litra mleka
mc = 0  # liczba litrów w cysternie
max_d = 3  # maksymalna liczba dni przez któe mleko może być u rolnika

old_milk_error_cost = 2000
dist_error_cost = 2000
volume_error_cost = 2000



################################################################## wersja 1

# SR = [
#     # [produkcja dzienna 0]
#     [50],
#     [100],
#     [20]
# ]


# # wszystkie "węzły" ( opróćz bazy, jest ona dodawana automatycznie)
# r = []
# r_size = len(SR)
# for i in range(r_size):
#     r.append(d_struct.Node("r", i))
#     r[i].data = SR[i]

# SM = [
#     # [(dni odbioru) 0 ,min 1, max 2, cena 3, kara umowan 4]
#     [(2, 5), 320, 500, 2, 500],
#     [(1, 3, 4), 100, 500, 3, 500]
# ]

# m = []
# m_size = 2
# for i in range(m_size):
#     m.append(d_struct.Node("m", i))
#     m[i].data = SM[i]


# b = d_struct.Node("b")

# node_list = [b] + r + m


# # macierz połączeń - dla uprosczenia założon, że z każdego punktu można pojechać do każdego innego
# connection = [[0, 2, 3, 4, 5, 6],
#               [2, 0, 3, 4, 5, 6],
#               [3, 3, 0, 4, 5, 6],
#               [4, 4, 4, 0, 5, 6],
#               [5, 5, 5, 5, 0, 6],
#               [6, 6, 6, 6, 6, 0]]

# G = d_struct.Neigbour_matrix()
# G.set_node_list(node_list)
# G.set_connection(connection)

# start_solution = [
#     [(b, 0), (r[0], 30), (r[1], 50), (m[1], 50), (r[2], 60)],
#     [(b, 0), (r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)],
#     [(b, 0), (r[0], 30), (r[1], 50), (r[2], 100), (m[0], 180)],
#     [(b, 0), (r[0], 30), (r[2], 50), (m[0], 50), (r[2], 60)],
#     [(b, 0), (r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)]]

################################################################## wersja 1
################################################################## wersja 2

#tworzenie SR
# [produkcja dzienna 0]
lr = 5 # liczba rolników
min_r_m = 20 # minimalna dzienna liczba produkowanych litrów mleka w gospodarstwie
max_r_m = 200 # maksymalna dzienna liczba produkowanych litrów mleka w gospodarstwie


def create_SR(lr, min_r_m, max_r_m):
    tab = []
    for i in range(lr):
        tab.append([random.randrange(min_r_m, max_r_m, 1)])
    return tab

# SR = create_SR(lr, min_r_m, max_r_m)
# print(SR)

#tworzenie SM
# [(dni odbioru) 0 ,min 1, max 2, cena 3, kara umowan 4]
lm = 3 # liczba mleczarnii
min_m_m = (100, 300) # zakres dla minimalnej ilości przyjmowanych litrów mleka
max_m_m = (500, 800) # zakres dla maksymalnej ilości przyjmowanych litrów mleka
c_range = (1, 5) # zakres cen za litr
k_range = (100, 500) # zakres kar umownych


def create_SM(lm, min_m_m, max_m_m, c_range, k_range):
    dni = [1, 2, 3, 4, 5]
    tab = []
    old = []
    for i in range(lm-1):
        she = []
        #losowanie dni dostaw
        for j in range(random.randrange(2, 4, 1)):
            d = random.randrange(1, 5, 1)
            she.append(d)
            old.append(d)
        min_il = random.randrange(min_m_m[0], min_m_m[1], 1)
        max_il = random.randrange(max_m_m[0], max_m_m[1], 1)
        c = random.randrange(c_range[0], c_range[1], 1)
        k = random.randrange(k_range[0], k_range[1], 1)
        tab.append([she, min_il, max_il, c, k])
    #tworzenie ostatniego elementu
    she=[]
    for ele in dni:
        if ele not in old:
            she.append(ele)
    if she == []:
        she = [1,3,5]
    min_il = random.randrange(min_m_m[0], min_m_m[1], 1)
    max_il = random.randrange(max_m_m[0], max_m_m[1], 1)
    c = random.randrange(c_range[0], c_range[1], 1)
    k = random.randrange(k_range[0], k_range[1], 1)
    tab.append([she, min_il, max_il, c, k])
    return tab

# SM = create_SM(lm, min_m_m, max_m_m, c_range, k_range)
# print(SM)

#tworzenie connection
l_ele = lr + lm + 1 #liczba węzłów grafu
con_range = (1, 10) #zakres połączeń między wierzchołkami


def create_conection(l_ele, con_range):
    #tworzenie macierzy
    tab_1 = []
    for i in range(l_ele):
        tab_2 = []
        for j in range(l_ele):
            tab_2.append(0) 
        tab_1.append(tab_2)
    #wypełnianie macierzy
    for i in range(l_ele):
        for j in range(l_ele):
            if i != j:
                distance = random.randrange(con_range[0], con_range[1], 1)
                tab_1[i][j] = distance
                tab_1[j][i] = distance

    return np.array(tab_1)

# conection = create_conection(l_ele, con_range)
# print(conection)


#tworzenie losowych danych
SR = create_SR(lr, min_r_m, max_r_m)
r = []
r_size = len(SR)
for i in range(r_size):
    r.append(d_struct.Node("r", i))
    r[i].data = SR[i]


SM = create_SM(lm, min_m_m, max_m_m, c_range, k_range)
m = []
m_size = len(SM)
for i in range(m_size):
    m.append(d_struct.Node("m", i))
    m[i].data = SM[i]


b = d_struct.Node("b")

node_list = [b] + r + m

connection = create_conection(l_ele, con_range)

G = d_struct.Neigbour_matrix()
G.set_node_list(node_list)
G.set_connection(connection)

start_solution = [
    [[b, 0], [r[0], 30],  [r[1], 50 ] ,[m[1], 50 ],  [r[2], 60 ]],
    [[b, 0], [r[1], 100], [r[0], 100], [m[1], 160],  [m[0], 40 ]],
    [[b, 0], [r[0], 30],  [r[1], 50 ], [r[2], 100],  [m[0], 180]],
    [[b, 0], [r[0], 30],  [r[2], 50 ], [m[0], 50 ],  [r[2], 60 ]],
    [[b, 0], [r[1], 100], [r[0], 100], [m[1], 160],  [m[0], 40 ]]]
################################################################## wersja 2





# funkcje
def how_much_milk_is_in_point(timetable: List[List[List]], day_nr: int, nr_in_day: int):  # ilość mleka na danym przystanku przed iterwencją wozu z mlekiem
    checked_node = timetable[day_nr][nr_in_day]

    if checked_node[0].name == 'b':
        milk_in_base = 0
        for day in timetable[:day_nr]:
            milk_on_car = 0
            for node in day:
                if node[0].name == 'b':
                    milk_in_base -= node[1] # minus ponieważ liczba w node mówi o tym ile  mleka trafiło do ciężarówki
                elif node[0].name == 'm':
                    milk_on_car -= node[1]
                elif node[0].name == 'r':
                    milk_in_base += node[1]
            milk_in_base += milk_on_car

        milk_on_car = 0

        for node in timetable[day_nr][:nr_in_day]:
            if node[0].name == 'b':
                milk_in_base -= node[1]  # minus ponieważ liczba w node mówi o tym ile  mleka trafiło do ciężarówki
            elif node[0].name == 'm':
                milk_on_car -= node[1]
            elif node[0].name == 'r':
                milk_in_base += node[1]
        milk_in_base += milk_on_car

        return milk_in_base
    elif checked_node[0].name == 'm':
        milk_in_dairy = 0
        for day in timetable[:day_nr]:
            for node in day:
                if node[0] == checked_node[0]:
                    milk_in_dairy += node[1]

        for node in timetable[day_nr][:nr_in_day]:
            if node[0] == checked_node[0]:
                milk_in_dairy += node[1]

        return milk_in_dairy
    elif checked_node[0].name == 'r':
        milk_at_farmer = checked_node[0].data[0] * (day_nr + 1) # założono, że w poniedzaiłek farmy mają mleko z jednego dnia
        for day in timetable[:day_nr]:
            for node in day:
                if node[0] == checked_node[0]:
                    milk_at_farmer -= node[1]

        for node in timetable[day_nr][:nr_in_day]:
            if node[0] == checked_node[0]:
                milk_at_farmer -= node[1]
        return milk_at_farmer
import struct
import numpy as np

# Główne dane:
lk = 20  # limit kilonmetrów
pc = 200  # pojemność cysterny
cp = 0.1  # cena przejazdu jednego kilonmetra
cs = 0.2  # cena schłodzenia jednego litra mleka
mc = 0  # liczba litrów w cysternie
max_d = 3  # maksymalna liczba dni przez któe mleko może być u rolnika

# zmienne do obliczania zysku
k = 0  # kary umowne
p = 0  # koszt paliwa

# wszystkie "węzły" ( opróćz bazy, jest ona dodawana automatycznie)
r = []
r_size = 3
for i in range(r_size):
    r.append(struct.Node("r", i))

m = []
m_size = 2
for i in range(r_size):
    r.append(struct.Node("m", i))

b = struct.Node("b")

node_list = r + m + [b]

# macierz połączeń - dla uprosczenia założon, że z każdego punktu można pojechać do każdego innego
connection = np.array([[1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6]])

SR = [
    # [produkcja dzienna, aktualna liczba mleka, jak dawno mleko nie było odbierane, cena skupu]
    [50, 100, 2, 1.2],
    [100, 200, 4, 1.3],
    [20, 30, 1, 1.2]
]

SM = [
    # [(dni odbioru),min, max, cena, kara umowan, zgroamdzone mleko ]
    [(2, 5), 100, 500, 2.5, 1000, 0],
    [(1, 3, 4), 100, 500, 2, 1000, 0]
]

rozw_start = [
    [(r[0], 30), (r[1], 50), (m[1], 50), (r[2], 60)],
    [(r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)],
    [(r[0], 30), (r[1], 50), (r[2], 100), (m[0], 180)],
    [(r[0], 30), (r[2], 50), (m[0], 50), (r[2], 60)],
    [(r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)]]

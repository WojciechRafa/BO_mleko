import struct
import numpy as np

# Główne dane:
lk = 20     # limit kilonmetrów
pc = 200    # pojemność cysterny
cp = 0.1    # cena przejazdu jednego kilonmetra
cs = 0.2    # cena schłodzenia jednego litra mleka
mc = 0      # liczba litrów w cysternie
max_d = 3   # maksymalna liczba dni przez któe mleko może być u rolnika

            # zmienne do obliczania zysku
k = 0       # kary umowne
p = 0       # koszt paliwa

# wszystkie "węzły" ( opróćz bazy, jest ona dodawana automatycznie)
r_1 = struct.Node("r", 1)
r_2 = struct.Node("r", 2)
r_3 = struct.Node("r", 3)
m_1 = struct.Node("m", 1)
m_2 = struct.Node("m", 2)
b = struct.Node("b")

node_list = [r_1, r_2, r_3, m_1, m_2]

# macierz połączeń - dla uprosczenia założon, że z każdego punktu można pojechać do każdego innego
connection = np.array([[1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6],
                       [1, 2, 3, 4, 5, 6]])

SM = [
    #[(dni odbioru),min, max, cena, kara umowan, zgroamdzone mleko ]
    [(2, 5), 100, 500, 2.5, 1000, 0],
    [(1, 3, 4), 100, 500, 2, 1000, 0]
]

SR = [
    # [produkcja dzienna, aktualna liczba mleka, jak dawno mleko nie było odbierane, cena skupu]
    [50, 100, 2, 1.2],
    [100, 200, 4, 1.3],
    [20, 30, 1, 1.2]
]


rozw_start = [
    [(r_1, 30), (r_2, 50), (m_1, 50), (r_3, 60)],
    [(r_2, 100), (r_1, 100), (m_2, 160), (m_1, 40)],
    [(r_1, 30), (r_2, 50), (r_3, 100), (m_1, 180)],
    [(r_1, 30), (r_2, 50), (m_1, 50), (r_3, 60)],
    [(r_2, 100), (r_1, 100), (m_2, 160), (m_1, 40)]]
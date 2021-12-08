import struct


print("AAA")

# Główne dane:
lk = 20  # limit kilonmetrów
pc = 200  # pojemność cysterny
cp = 0.1  # cena przejazdu jednego kilonmetra
cs = 0.2  # cena schłodzenia jednego litra mleka
mc = 0  # liczba litrów w cysternie
max_d = 3  # maksymalna liczba dni przez któe mleko może być u rolnika

old_milk_error_cost = 2000
dist_error_cost = 2000
volume_error_cost = 2000


SR = [
    # [produkcja dzienna 0 , aktualna liczba mleka 1 , jak dawno mleko nie było odbierane 2 ]
    [50, 100, 2],
    [100, 200, 4],
    [20, 30, 1]
]


# wszystkie "węzły" ( opróćz bazy, jest ona dodawana automatycznie)
r = []
r_size = 3
for i in range(r_size):
    r.append(struct.Node("r", i))
    r[i].data = SR[i]

SM = [
    # [(dni odbioru) 0 ,min 1, max 2, cena 3, kara umowan 4, zgroamdzone mleko 5]
    [(2, 5), 100, 500, 2.5, 1000, 0],
    [(1, 3, 4), 100, 500, 2, 1000, 0]
]

m = []
m_size = 2
for i in range(m_size):
    m.append(struct.Node("m", i))
    m[i].data = SM[i]


b = struct.Node("b")

node_list = [b] + r + m


# macierz połączeń - dla uprosczenia założon, że z każdego punktu można pojechać do każdego innego
connection = [[0, 2, 3, 4, 5, 6],
              [2, 0, 3, 4, 5, 6],
              [3, 3, 0, 4, 5, 6],
              [4, 4, 4, 0, 5, 6],
              [5, 5, 5, 5, 0, 6],
              [6, 6, 6, 6, 6, 0]]

G = struct.Neigbour_matrix()
G.set_node_list(node_list)
G.set_connection(connection)

start_solution = [
    [(b, 0), (r[0], 30), (r[1], 50), (m[1], 50), (r[2], 60)],
    [(b, 0), (r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)],
    [(b, 0), (r[0], 30), (r[1], 50), (r[2], 100), (m[0], 180)],
    [(b, 0), (r[0], 30), (r[2], 50), (m[0], 50), (r[2], 60)],
    [(b, 0), (r[1], 100), (r[0], 100), (m[1], 160), (m[0], 40)]]

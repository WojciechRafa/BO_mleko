import numpy as np
from typing import List


class Node:
    def __init__(self, name_, nr_=-1):
        self.name: str  # b - baza, f - farma, m - mleczarnia
        self.nr: int  # numeracja od 1

        if name_ != "b" and name_ != "f" and name_ != "m":
            raise Exception("niewlasciwa nazwa węzła")

        self.name = name_
        if name_ == 'b':
            self.nr = 1
        elif nr_ != -1:
            self.nr = nr_
        else:
            raise Exception("niewlasciwy numer węzła")

    def __eq__(self, other) -> bool:
        if self.name == other.name and self.nr == other.nr:
            return True
        else:
            return False

    def __str__(self):
        return str(self.name)+", "+str(self.nr)


class Neigbour_matrix:
    def __init__(self):
        self.node_list: List[Node] = [Node('b')]
        self.neighbour_array = np.array([])

    def set_node_list(self, node_list_):
        sorted(node_list_, key=lambda node: node[0])
        for node_tuple in in_data:
            self.node_list.append(Node(node_tuple[0], node_tuple[1]))

    def get_node_idx(self, node) -> int:
        for i in range(len(self.node_list)):
            if self.node_list[i] == node:
                return i
        raise Exception("Nie ma takiego węzła")

    def set_connection(self, conn_array: np.array):
        shape = conn_array.shape
        if (not shape[0] is shape[1]) or (not shape[0] is len(self.node_list)):
            raise Exception("Niewłaściwy rozmiar macierzy")
        self.neighbour_array = conn_array

    def print_nodes(self):
        for node in self.node_list:
            print(node)
        print("\n")

SM = {
    #[(dni odbioru),min, max, cena, kara umowan, zgroamdzone mleko ]
    Node('m', 1): [(2, 5), 100, 500, 2.5, 1000, 0],
    Node('m', 2): [(1,3, 4), 100, 500, 2, 1000, 0]
}

RM = {
    #[(dni odbioru),min, max, cena, kara umowan, zgroamdzone mleko ]
    Node('r', 1): [50,100,0],
    Node('r', 2): [100,200,0],
    Node('r', 3): [20,30,1]
}

if __name__ == '__main__':

    # Główne dane:
    # wszystkie "węzły" ( opróćz bazy, jest ona dodawana automatycznie)
    in_data =  (("f", 1),
                ("f", 2),
                ("f", 3),
                ("m", 1),
                ("m", 2))
    # macierz połączeń - dla uprosczenia założon, że z każdego punktu można pojechać do każdego innego
    connection = np.array([[1, 2, 3, 4, 5, 6],
                           [1, 2, 3, 4, 5, 6],
                           [1, 2, 3, 4, 5, 6],
                           [1, 2, 3, 4, 5, 6],
                           [1, 2, 3, 4, 5, 6],
                           [1, 2, 3, 4, 5, 6]])
    lk = 20     # limit kilonmetrów
    pc = 200    # pojemność cysterny
    cp = 0.1    # cena przejazdu jednego kilonmetra
    cs = 0.2    # cena schłodzenia jednego litra mleka
    mc = 0      # liczba litrów w cysternie
    max_d = 3   # maksymalna liczba dni przez któ©e mleko może być u rolnika

    R = [[], [], [], [], [], []]    # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    #



    G = Neigbour_matrix()
    G.set_node_list(in_data)
    G.print_nodes()

    G.set_connection(connection)




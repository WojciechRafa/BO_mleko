import numpy as np
from typing import List
from typing import Tuple

class Node:
    def __init__(self, name_, nr_=-1):
        self.name: str  # b - baza, r - farma, m - mleczarnia
        self.nr: int  # numeracja od 1

        if name_ != "b" and name_ != "r" and name_ != "m":
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
        #sorted(node_list_, key=lambda node: node.name)
        for node in node_list_:
            self.node_list.append(node)

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
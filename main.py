import numpy as np
from typing import List
from typing import Tuple

import data
import struct

if __name__ == '__main__':
    R = [[], [], [], [], [], []]  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu

    G = struct.Neigbour_matrix()
    G.set_node_list(data.node_list)
    G.print_nodes()

    G.set_connection(data.connection)
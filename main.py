from typing import List
from typing import Tuple

import data
import d_struct
import steps

if __name__ == '__main__':
    R = []  # rozwiązanie jest listą 5-ciu list krotek zawierających obiekt typu node i ilość mleka wlaną/wylaną w danym miejscu
    R = data.start_solution

    changes = steps.get_random_steps(R, 5)
    print("Elo")

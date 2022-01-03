from enum import IntEnum, auto
import random
from typing import List
from typing import Tuple

import data
import features

class Step_type(IntEnum):
    add_R = auto()
    add_M = auto()
    add_B = auto()

    remove_R = auto()
    remove_M = auto()
    remove_B = auto()

    increase_R = auto()
    decrease_R = auto()
    take_max_R = auto()

    increase_M = auto()
    decrease_M = auto()
    take_max_M = auto()
    take_min_M = auto()

    increase_B = auto()
    decrease_B = auto()


def __make_step(move_type: Step_type, day: List[Tuple])-> Tuple[bool, List]:    #funkcja zwaraca inoframcje o tym czy można wykonać funkcję oraz listę z dodatkowymi informacjami
    is_step_correct = True

    # dodanie nowego elemntu
    if move_type == Step_type.add_R:
        pos = random.randrange(len(day)) + 1
        r_nr = random.randrange(len(data.r))
        return True, [pos, data.r[r_nr]]

    elif move_type == Step_type.add_M:
        pos = random.randrange(len(day)) + 1
        m_nr = random.randrange(len(data.r))
        return True, [pos, data.m[m_nr]]

    elif move_type == Step_type.add_B:
        pos = random.randrange(len(day)) + 1
        return True, [pos, data.b]

    # usuwanie
    elif move_type == Step_type.remove_R:
        list_pos = []
        for i in range(len(day)):
            if day[i][0] in data.r:
                list_pos.append(i)

        if len(list_pos) == 0:
            return False, []
        else:
            return True, [list_pos[random.randrange(len(list_pos))]]
    elif move_type == Step_type.remove_M:
        list_pos = []
        for i in range(len(day)):
            if day[i][0] in data.r:
                list_pos.append(i)

        if len(list_pos) == 0:
            return False, []
        else:
            return True, [list_pos[random.randrange(len(list_pos))]]
    elif move_type == Step_type.remove_B:
        list_pos = []
        for i in range(len(day)):
            if day[i][0] in data.r:
                list_pos.append(i)

        if len(list_pos) == 0:
            return False, []
        else:
            return True, [list_pos[random.randrange(len(list_pos))]]

    elif move_type == Step_type.increase_R:
        r_list = []
        for i in range(len(day)):
            if [0][i] in data.r:
                r_list.append(i)

        if len(r_list) == 0:
            return False, []
        else:
            chosed_node = r_list[random.randrange(len(r_list))]
            milk_on_car = features.sum_milk(day[:chosed_node])
            max_added_milk = max(data.pc - milk_on_car, day[i][1])
            return True, []

    elif move_type == Step_type.decrease_R:
        pass
    elif move_type == Step_type.take_max_R:
        pass
    elif move_type == Step_type.increase_M:
        pass
    elif move_type == Step_type.decrease_M:
        pass
    elif move_type == Step_type.take_max_M:
        pass
    elif move_type == Step_type.take_min_M:
        pass
    elif move_type == Step_type.increase_B:
        pass
    elif move_type == Step_type.decrease_B:
        pass


class Step:
    def __init__(self, type_, day_: int):
        self.type = type_
        self.dat: int = day_

    def get_random_steps(self, R: List[Tuple], n: int) -> List:
        #imposible_move_list = []   # lista ta ma na celu ochronę przed wykonywaniem niemożliwych ruchów, posada ona w
        move_list = []

        while len(move_list) < n:
            # losowanie ruchu z listy enum ( lista jest numerowana od 1 więc dodano 1 )
            #move_type: Step_type = Step_type(random.randrange(int(Step_type.decrease_B)+1))

            # tymczasowo
            move_type: Step_type = Step_type(random.randrange(int(Step_type.add_B)+1))
            day_nr: int = random.randrange(5)
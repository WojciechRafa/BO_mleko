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

    increase_B = auto()# zwiększanie ilości mleka zabieranego do auta
    decrease_B = auto()


class Step:
    def __init__(self, type_, day_: int):
        self.type = type_
        self.day: int = day_
        self.is_posible: int = False
        self.data = []

    def detail_step(self, timetable: List[List[Tuple]], day_nr: int) -> Tuple[bool, List]:  # funkcja zwaraca inoframcje o tym czy można wykonać funkcję oraz listę z dodatkowymi informacjami
        to_return = None
        day: List[Tuple] = timetable[day_nr]

        # dodanie nowego elemntu
        if self.type == Step_type.add_R:
            pos = random.randrange(len(day)) + 1
            r_nr = random.randrange(len(data.r))
            to_return = True, [pos, data.r[r_nr]]

        elif self.type == Step_type.add_M:
            pos = random.randrange(len(day)) + 1
            m_nr = random.randrange(len(data.m))
            to_return = True, [pos, data.m[m_nr]]

        elif self.type == Step_type.add_B:
            pos = random.randrange(len(day)) + 1
            to_return = True, [pos, data.b]

        # usuwanie
        elif self.type == Step_type.remove_R:
            list_pos = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, []
            else:
                to_return = True, [list_pos[random.randrange(len(list_pos))]]
        elif self.type == Step_type.remove_M:
            list_pos = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, []
            else:
                to_return = True, [list_pos[random.randrange(len(list_pos))]]
        elif self.type == Step_type.remove_B:
            list_pos = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, []
            else:
                to_return = True, [list_pos[random.randrange(len(list_pos))]]

        elif self.type == Step_type.increase_R:
            r_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    r_list.append(i)

            if len(r_list) == 0:
                to_return = False, []
            else:
                chosed_node: int = r_list[random.randrange(len(r_list))]
                milk_on_car = features.sum_milk(day[:chosed_node])

                car_limit: int = data.pc - milk_on_car
                farmer_limit: int = data.how_many_milk_is_in_point(timetable, self.day, chosed_node) - day[chosed_node][1]

                max_added_milk = 0
                if car_limit > 0 and farmer_limit > 0:
                    max_added_milk = max(car_limit, farmer_limit)
                elif car_limit > 0:
                    max_added_milk = car_limit
                elif farmer_limit > 0:
                    max_added_milk = farmer_limit
                else:
                    max_added_milk = data.pc  # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami

                to_return = True, [chosed_node, random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_R:
            to_return = False, []  # TODO

        elif self.type == Step_type.take_max_R:
            to_return = False, []  # TODO

        elif self.type == Step_type.increase_M:
            m_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.m:
                    m_list.append(i)

            if len(m_list) == 0:
                to_return = False, []
            else:
                chosed_node: int = m_list[random.randrange(len(m_list))]
                milk_on_car: int = features.sum_milk(day[:chosed_node])

                car_limit: int = milk_on_car - day[chosed_node][1]

                max_added_milk = 0
                if car_limit > 0:
                    max_added_milk = car_limit
                else:
                    max_added_milk = day[chosed_node][0].data[2]  # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami

                to_return = True, [chosed_node, random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_M:
            to_return = False, []  # TODO
        elif self.type == Step_type.take_max_M:
            to_return = False, []  # TODO
        elif self.type == Step_type.take_min_M:
            to_return = False, []  # TODO

        elif self.type == Step_type.increase_B:
            b_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] == data.b:
                    b_list.append(i)

            if len(b_list) == 0:
                to_return = False, []
            else:
                chosed_node: int = b_list[random.randrange(len(b_list))]
                milk_on_car: int = features.sum_milk(day[:chosed_node])

                car_limit: int = milk_on_car - day[chosed_node][1]

                max_added_milk = 0
                if car_limit > 0:
                    max_added_milk = car_limit
                else:
                    max_added_milk = data.pc
                to_return = True, [chosed_node, random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_B:
            to_return = False, []  # TODO

        self.is_posible = to_return[0]
        self.data = to_return[1]

        return to_return


def get_random_steps(timetable: List[List[Tuple]], n: int, max_fail_nr: int = 20) -> List:
    imposible_move_list = []   # lista ta ma na celu ochronę przed wykonywaniem niemożliwych ruchów, posiada ona w
    move_list = []
    while len(move_list) < n:
        # losowanie ruchu z listy enum ( lista jest numerowana od 1 więc dodano 1 )
        step_type_nr = random.randrange(len(Step_type))
        move_type: Step_type = Step_type(step_type_nr + 1)  # auto w enum numeruje od 1
        day_nr: int = random.randrange(5)
        if (move_type, day_nr) in imposible_move_list:
            imposible_move_list.append((move_type, day_nr))
        else:
            step: Step = Step(move_type, day_nr)
            is_posible, step_data = step.detail_step(timetable, day_nr)
            if not is_posible:
                imposible_move_list.append((move_type, day_nr))
            else:
                move_list.append(step)
        if len(imposible_move_list) > max_fail_nr:
            break

    return move_list

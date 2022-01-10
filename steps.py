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
    increase_M = auto()
    increase_B = auto()  # zwiększanie ilości mleka zabieranego do auta

    decrease_R = auto()
    decrease_M = auto()
    decrease_B = auto()

    take_max_R = auto()
    take_max_M = auto()
    take_min_M = auto()


class Step:
    def __init__(self, type_, day_: int):
        self.type = type_
        self.day: int = day_
        self.node_in_day: int = -1
        self.is_posible: int = False
        self.data = []

    def detail_step(self, timetable: List[List[List]], day_nr: int) -> Tuple[
        bool, int, List]:  # funkcja zwaraca inoframcje o tym czy można wykonać funkcję oraz listę z dodatkowymi informacjami
        to_return = None
        day: List[List] = timetable[day_nr]

        # dodanie nowego elemntu
        if self.type == Step_type.add_R:
            pos = random.randrange(len(day)) + 1
            r_nr = random.randrange(len(data.r))
            milk_on_car = features.sum_milk(day[:pos])

            car_limit: int = data.pc - milk_on_car
            farmer_limit: int = data.how_much_milk_is_in_point(timetable, self.day, pos - 1) - day[pos - 1][1]

            max_added_milk = 0
            if car_limit > 0 and farmer_limit > 0:
                max_added_milk = max(car_limit, farmer_limit)
            elif car_limit > 0:
                max_added_milk = car_limit
            elif farmer_limit > 0:
                max_added_milk = farmer_limit
            else:
                max_added_milk = data.pc  # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami
            to_return = True, pos, [data.r[r_nr], random.randrange(max_added_milk)]

        elif self.type == Step_type.add_M:
            pos = random.randrange(len(day)) + 1
            m_nr = random.randrange(len(data.m))

            milk_on_car: int = features.sum_milk(day[:pos])
            car_limit: int = milk_on_car - day[pos - 1][1]

            max_added_milk = 0
            if car_limit > 0:
                max_added_milk = car_limit
            else:
                max_added_milk = data.m[m_nr].data[2]  # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami

            to_return = True, pos, [data.m[m_nr], random.randrange(max_added_milk)]

        elif self.type == Step_type.add_B:
            pos = random.randrange(len(day)) + 1

            milk_on_car: int = features.sum_milk(day[:pos])
            car_limit: int = milk_on_car - day[pos - 1][1]

            if car_limit > 0:
                to_return = True, pos, [data.b, random.randrange(car_limit)]
            else:
                to_return = True, pos, [data.b, (-1) * random.randrange(milk_on_car)]


        # usuwanie
        elif self.type == Step_type.remove_R:
            list_pos = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, None, []
            else:
                to_return = True, list_pos[random.randrange(len(list_pos))], []
        elif self.type == Step_type.remove_M:
            list_pos = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, None, []
            else:
                to_return = True, list_pos[random.randrange(len(list_pos))], []
        elif self.type == Step_type.remove_B:
            list_pos = []
            for i in range(1, len(day)):
                if day[i][0] in data.r:
                    list_pos.append(i)

            if len(list_pos) == 0:
                to_return = False, None, []
            else:
                to_return = True, list_pos[random.randrange(len(list_pos))], []

        elif self.type == Step_type.increase_R:
            r_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    r_list.append(i)

            if len(r_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = r_list[random.randrange(len(r_list))]
                milk_on_car = features.sum_milk(day[:chosed_node])

                car_limit: int = data.pc - milk_on_car
                farmer_limit: int = data.how_much_milk_is_in_point(timetable, self.day, chosed_node) - day[chosed_node][
                    1]

                max_added_milk = 0
                if car_limit > 0 and farmer_limit > 0:
                    max_added_milk = max(car_limit, farmer_limit)
                elif car_limit > 0:
                    max_added_milk = car_limit
                elif farmer_limit > 0:
                    max_added_milk = farmer_limit
                else:
                    max_added_milk = data.pc  # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami

                to_return = True, chosed_node, [random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_R:
            r_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    r_list.append(i)

            if len(r_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = r_list[random.randrange(len(r_list))]
                max_decrease = timetable[self.day][chosed_node][1]
                to_return = True, chosed_node, [random.randrange(max_decrease)]

        elif self.type == Step_type.take_max_R:  # w data podawana jest maksymalna wartość jaka może być doładowana (jeżeli ma wartość ujemną to jest ona wyładowywana)
            r_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.r:
                    r_list.append(i)

            if len(r_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = r_list[random.randrange(len(r_list))]
                milk_on_car = features.sum_milk(day[:chosed_node + 1])

                car_limit: int = data.pc - milk_on_car
                milk_in_point = data.how_much_milk_is_in_point(timetable, self.day, chosed_node)
                farmer_limit: int = milk_in_point - day[chosed_node][1]

                is_added = True

                max_added_milk = 0
                max_removed_milk = 0

                if car_limit > 0 and farmer_limit > 0:
                    max_added_milk = max(car_limit, farmer_limit)
                elif car_limit > 0:
                    max_added_milk = car_limit
                elif farmer_limit > 0:
                    max_added_milk = farmer_limit
                else:
                    is_added = False

                if not is_added:
                    max_removed_milk = day[chosed_node][1] - milk_in_point

                if is_added:
                    to_return = True, chosed_node, [max_added_milk]
                else:
                    to_return = True, chosed_node, [max_removed_milk * (-1)]  # jeżeli nie ma możliwości dokonania ruchu

        elif self.type == Step_type.increase_M:
            m_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.m:
                    m_list.append(i)

            if len(m_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = m_list[random.randrange(len(m_list))]
                milk_on_car: int = features.sum_milk(day[:chosed_node])

                car_limit: int = milk_on_car - day[chosed_node][1]

                max_added_milk = 0
                if car_limit > 0:
                    max_added_milk = car_limit
                else:
                    # jeżeli nie ma możliwości dokonania ruchu tak aby znalazł się on w limitach wykonujemy ruch poza tymi limitami
                    max_added_milk = day[chosed_node][0].data[2] // 2

                to_return = True, chosed_node, [random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_M:
            m_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.m:
                    m_list.append(i)

            if len(m_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = m_list[random.randrange(len(m_list))]
                max_decrease = timetable[self.day][chosed_node][1]
                to_return = True, chosed_node, [random.randrange(max_decrease)]

        elif self.type == Step_type.take_max_M:
            m_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.m:
                    m_list.append(i)

            if len(m_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = m_list[random.randrange(len(m_list))]
                max_milk_to_node = timetable[self.day][chosed_node][0].data[2]
                milk_in_dairy = data.how_much_milk_is_in_point(timetable, self.day, chosed_node)
                milk_on_car = features.sum_milk(day[:chosed_node + 1])
                if milk_in_dairy <= max_milk_to_node:
                    to_return = True, chosed_node, [max_milk_to_node - milk_in_dairy]
                else:
                    to_return = True, chosed_node, [milk_in_dairy - milk_on_car]

        elif self.type == Step_type.take_min_M:
            m_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] in data.m:
                    m_list.append(i)

            if len(m_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = m_list[random.randrange(len(m_list))]
                max_milk_to_node = timetable[self.day][chosed_node][0].data[1]
                milk_in_dairy = data.how_much_milk_is_in_point(timetable, self.day, chosed_node)
                milk_on_car = features.sum_milk(day[:chosed_node + 1])
                if milk_in_dairy <= max_milk_to_node:
                    to_return = True, chosed_node, [max_milk_to_node - milk_in_dairy]
                else:
                    to_return = True, chosed_node, [milk_in_dairy - milk_on_car]

        elif self.type == Step_type.increase_B:
            b_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] == data.b:
                    b_list.append(i)

            if len(b_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = b_list[random.randrange(len(b_list))]
                milk_on_car: int = features.sum_milk(day[:chosed_node])

                car_limit: int = milk_on_car - day[chosed_node][1]

                max_added_milk = 0
                if car_limit > 0:
                    max_added_milk = car_limit
                else:
                    max_added_milk = data.pc
                to_return = True, chosed_node, [random.randrange(max_added_milk)]

        elif self.type == Step_type.decrease_B:
            b_list: List[int] = []
            for i in range(len(day)):
                if day[i][0] == data.b:
                    b_list.append(i)

            if len(b_list) == 0:
                to_return = False, None, []
            else:
                chosed_node: int = b_list[random.randrange(len(b_list))]
                milk_on_car: int = features.sum_milk(day[:chosed_node])
                added_milk = timetable[self.day][chosed_node][1]

                limit = milk_on_car + added_milk

                max_decrase_milk = 0
                if limit > 0:
                    to_return = True, chosed_node, [random.randrange(limit)]
                else:
                    to_return = False, None, []

        self.is_posible = to_return[0]
        self.node_in_day = to_return[1]
        self.data = to_return[2]

        return to_return


def get_random_steps(timetable: List[List[Tuple]], n: int, max_fail_nr: int = 20) -> List:
    imposible_move_list = []  # lista ta ma na celu ochronę przed wykonywaniem niemożliwych ruchów, posiada ona w
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
            is_posible, moment_in_day, step_data = step.detail_step(timetable, day_nr)
            if not is_posible:
                imposible_move_list.append((move_type, day_nr))
            else:
                move_list.append(step)
        if len(imposible_move_list) > max_fail_nr:
            break

    return move_list


# day_nr i node_in_day odnaoszą się do pierwszego noda którego możemy modyfikować
# diff - ilość mleka która idzie na pojazd ( jeżeli jest minus to ilość mleka która wychodzi z pojazdu )
def update_timetable_after(timetable: List[List[List]], day_nr: int, node_in_day: int, milk_change: int) -> Tuple[bool, int]:
    print("after")
    print("milk change - {}".format(milk_change))
    day = day_nr
    if milk_change > 0:
        print("milk_change > 0")
        is_positive = True
        for i in range(node_in_day, len(timetable[day])):
            node = timetable[day][i][0]
            if node.name == 'm':
                timetable[day][i][1] += milk_change
                milk_change = 0
                break

            if node.name == 'r':
                if timetable[day][i][1] >= milk_change:
                    timetable[day][i][1] -= milk_change
                    milk_change = 0
                    break
                else:
                   # diff = milk_change - timetable[day][i][1]

                    milk_change -= timetable[day][i][1]
                    timetable[day][i][1] = 0

            if node.name == 'b':
                timetable[day][i][1] -= milk_change
                break

        #if milk_change > 0:
        #    for i_day in range(day_nr + 1, 5):
        #        day = i_day
        #        for i in range(len(timetable[day])):
        #            node = timetable[day][i][0]
        #            if node.name == 'm':
        #                timetable[day][i][1] += milk_change
        #                milk_change = 0
        #                break
#
        #            if node.name == 'r':
        #                if timetable[day][i][1] >= milk_change:
        #                    timetable[day][i][1] -= milk_change
        #                    milk_change = 0
        #                    break
        #                else:
        #                    diff = milk_change - timetable[day][i][1]
        #                    timetable[day][i][1] = 0
        #                    milk_change -= diff
#
        #            if node.name == 'b':
        #                timetable[day][i][1] -= milk_change
        #                break

    else:
        print("milk_change < 0")
        is_positive = False
        milk_change = abs(milk_change)  # !!! milk change -ile mleka musimy dodatkowo zdobyć
        day = day_nr
        for i in range(node_in_day, len(timetable[day])):
            node = timetable[day][i][0]
            if node.name == 'm':
                if timetable[day][i][1] >= milk_change:
                    timetable[day][i][1] -= milk_change
                    milk_change = 0
                    break
                else:
                    #diff = milk_change - timetable[day][i][1]

                    milk_change -= timetable[day][i][1]
                    timetable[day][i][1] = 0

            elif node.name == 'r':
                max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                if max_added >= milk_change:
                    timetable[day][i][1] += milk_change
                    milk_change = 0
                    break
                elif max_added > 0:
                    #diff = milk_change - max_added
                    timetable[day][i][1] = 0
                    milk_change -= max_added

            elif node.name == 'b':
                max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                if max_added >= milk_change:
                    timetable[day][i][1] += milk_change
                    milk_change = 0
                    break
                else:
                   # diff = milk_change - max_added
                    timetable[day][i][1] += max_added
                    milk_change -= max_added

        if milk_change > 0:
            for i_day in range(day_nr + 1, 5):
                day = i_day
                had_break = False
                for i in range(len(timetable[day])):
                    node = timetable[day][i][0]
                    if node.name == 'm':
                        if timetable[day][i][1] >= milk_change:
                            timetable[day][i][1] -= milk_change
                            milk_change = 0
                            break
                        else:
                            #diff = milk_change - timetable[day][i][1]

                            milk_change -= timetable[day][i][1]
                            timetable[day][i][1] = 0

                    if node.name == 'r':
                        max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                        if max_added >= milk_change:
                            timetable[day][i][1] += milk_change
                            milk_change = 0
                            break
                        elif max_added > 0:
                            #diff = milk_change - max_added
                            timetable[day][i][1] = 0
                            milk_change -= max_added

                    if node.name == 'b':
                        max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                        if max_added >= milk_change:
                            timetable[day][i][1] += milk_change
                            milk_change = 0
                            break
                        else:
                            #diff = milk_change - max_added
                            timetable[day][i][1] += max_added

                            milk_change -= max_added
    if not is_positive:
        milk_change = milk_change * (-1)

    if milk_change > 0:
        return False, milk_change
    else:
        return True, milk_change


# day_nr i node_in_day odnaoszą się do pierwszego noda przed ostatnim który możemy modyfikować
# diff - ilość mleka która idzie na pojazd ( jeżeli jest minus to ilość mleka która wychodzi z pojazdu )
def update_timetable_before(timetable: List[List[List]], day_nr: int, node_in_day: int, milk_change: int) -> Tuple[
    bool, int]:
    print("before")
    print("milk change - {}".format(milk_change))
    is_positive = True
    day = day_nr
    if milk_change > 0:
        print("milk_change > 0")
        for i in reversed(range(node_in_day)):  # użycie reversed z jakiś powodów wywołuje warrninga poniżej
            node = timetable[day][i][0]
            if node.name == 'm':
                timetable[day][i][1] += milk_change
                milk_change = 0
                break

            if node.name == 'r':
                if timetable[day][i][1] >= milk_change:
                    timetable[day][i][1] -= milk_change
                    milk_change = 0
                    break
                else:
                    #diff = milk_change - timetable[day][i][1]
                    milk_change -= timetable[day][i][1]
                    timetable[day][i][1] = 0

            if node.name == 'b':
                timetable[day][i][1] -= milk_change
                break

        if milk_change > 0:
            for i_day in reversed(range(day_nr)):
                day = i_day
                for i in reversed(range(len(timetable[day]))):
                    node = timetable[day][i][0]
                    if node.name == 'm':
                        timetable[day][i][1] += milk_change
                        milk_change = 0
                        break

                    if node.name == 'r':
                        if timetable[day][i][1] >= milk_change:
                            timetable[day][i][1] -= milk_change
                            milk_change = 0
                            break
                        else:
                            #diff = milk_change - timetable[day][i][1]

                            milk_change -= timetable[day][i][1]
                            timetable[day][i][1] = 0

                    if node.name == 'b':
                        timetable[day][i][1] -= milk_change
                        break

    else:
        print("milk_change < 0")
        is_positive = False
        milk_change = abs(milk_change)  # !!! milk change -ile mleka musimy dodatkowo zdobyć
        day = day_nr
        for i in reversed(range(node_in_day)):
            node = timetable[day][i][0]
            if node.name == 'm':
                if timetable[day][i][1] >= milk_change:
                    timetable[day][i][1] -= milk_change
                    milk_change = 0
                    break
                else:
                    #diff = milk_change - timetable[day][i][1]

                    milk_change -= timetable[day][i][1]
                    timetable[day][i][1] = 0

            if node.name == 'r':
                max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                if max_added >= milk_change:
                    timetable[day][i][1] += milk_change
                    milk_change = 0
                    break
                elif max_added > 0:
                    #diff = milk_change - max_added
                    timetable[day][i][1] = 0
                    milk_change -= max_added

            if node.name == 'b':
                max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                if max_added >= milk_change:
                    timetable[day][i][1] += milk_change
                    milk_change = 0
                    break
                else:
                    #diff = milk_change - max_added
                    timetable[day][i][1] += max_added
                    milk_change -= max_added

        if milk_change > 0:
            for i_day in range(day_nr + 1, 5):
                day = i_day
                for i in range(len(timetable[day])):
                    node = timetable[day][i][0]
                    if node.name == 'm':
                        if timetable[day][i][1] >= milk_change:
                            timetable[day][i][1] -= milk_change
                            milk_change = 0
                            break
                        else:
                            #diff = milk_change - timetable[day][i][1]
                            milk_change -= timetable[day][i][1]
                            timetable[day][i][1] = 0


                    if node.name == 'r':
                        max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                        if max_added >= milk_change:
                            timetable[day][i][1] += milk_change
                            milk_change = 0
                            break
                        elif max_added > 0:
                            #diff = milk_change - max_added
                            timetable[day][i][1] = 0
                            milk_change -= max_added

                    if node.name == 'b':
                        max_added = data.how_much_milk_is_in_point(timetable, day, i) - timetable[day][i][1]
                        if max_added >= milk_change:
                            timetable[day][i][1] += milk_change
                            milk_change = 0
                            break
                        else:
                            #diff = milk_change - max_added
                            timetable[day][i][1] += max_added
                            milk_change -= max_added

    if not is_positive:
        milk_change = milk_change * (-1)

    if milk_change > 0:
        return False, milk_change
    else:
        return True, milk_change


def update_time_table(timetable: List[List[List]], step: Step, milk):
    if random.choice([True, False]):
        is_correct = False
        if step.node_in_day + 1 >= len(timetable[step.day]):  # kolejny element nie znaduje się w tym samym dniu
            if step.day < 4:  # czy to ostatni dzień tygodnia
                is_correct, rest_of_milk = update_timetable_after(timetable, step.day + 1, 0, milk)
        else:
            is_correct, rest_of_milk = update_timetable_after(timetable, step.day, step.node_in_day, milk)

        if not is_correct:
            is_correct, rest_of_milk = update_timetable_before(timetable, step.day, step.node_in_day, milk)
    else:
        is_correct, rest_of_milk = update_timetable_before(timetable, step.day, step.node_in_day, milk)
        if not is_correct:
            if step.node_in_day + 1 >= len(timetable[step.day]):  # kolejny element nie znaduje się w tym samym dniu
                if step.day < 4:  # czy to ostatni dzień tygodnia
                    is_correct, rest_of_milk = update_timetable_after(timetable, step.day + 1, 0, milk)
            else:
                is_correct, rest_of_milk = update_timetable_after(timetable, step.day, step.node_in_day, milk)


def make_timetable_copy(timetable: List[List[List]]) -> List[List[List]]:
    result = []
    for day in timetable:
        result.append(day[:])
    return result


def make_step(timetable: List[List[List]], step: Step) -> List[List[List]]:
    if step.type == Step_type.add_R or step.type == Step_type.add_M or step.type == Step_type.add_B:
        timetable[step.day].insert(step.node_in_day, [step.data[0], step.data[1]])
        if step.type == Step_type.add_R or step.type == Step_type.add_B:
            milk = step.data[1]
        else:
            milk = step.data[1] * (-1)

        update_time_table(timetable, step, milk)

    elif step.type == Step_type.remove_R or step.type == Step_type.remove_M or step.type == Step_type.remove_B:
        milk = timetable[step.day][step.node_in_day][1]
        del timetable[step.day][step.node_in_day]

        if step.type == Step_type.remove_R or step.type == Step_type.remove_B:
            milk = milk * (-1)

        update_time_table(timetable, step, milk)

    elif step.type == Step_type.increase_R or step.type == Step_type.increase_M or step.type == Step_type.increase_B:

        timetable[step.day][step.node_in_day][1] += step.data[0]
        if step.type == Step_type.increase_R or step.type == Step_type.increase_B:
            milk = step.data[0]
        else:
            milk = step.data[0] * (-1)

        update_time_table(timetable, step, milk)

    elif step.type == Step_type.decrease_R or step.type == Step_type.decrease_M or step.type == Step_type.decrease_B:

        timetable[step.day][step.node_in_day][1] -= step.data[0]
        if step.type == Step_type.decrease_R or step.type == Step_type.decrease_B:
            milk = step.data[0] * (-1)
        else:
            milk = step.data[0]

        update_time_table(timetable, step, milk)

    elif step.type == Step_type.take_max_R:
        timetable[step.day][step.node_in_day][1] += step.data[0]
        milk = step.data[0]
        update_time_table(timetable, step, milk)

    elif step.type == Step_type.take_max_M or step.type == Step_type.take_min_M:
        timetable[step.day][step.node_in_day][1] += step.data[0]
        milk = step.data[0]
        update_time_table(timetable, step, milk*(-1))

    return timetable

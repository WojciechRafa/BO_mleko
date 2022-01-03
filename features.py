from typing import Tuple
from typing import List

import data


#def sum_by_day(solution: List, foo):
#    sum = 0
#    for day in solution:
#        for node_and_milk in day:
#            sum += foo(node_and_milk)
#    return sum


def sum_milk(nodes: List):
    milk = 0
    for node in nodes:
        if node[0].name == 'm':
            milk -= node[1]
        else:
            milk += node[1] # założono, że w przypadku bazy plusem oznaczony jest załadunke na pojazd

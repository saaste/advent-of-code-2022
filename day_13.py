from typing import Any, List, Optional, Tuple, Union
from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file, read_as_str_list
from utils.test import is_test_run
from functools import cmp_to_key
SOLUTION_1 = 5196
SOLUTION_2 = 22134

def check_int(left: int, right: int, depth: int = 1) -> Optional[bool]:
    #print(f"{'  ' * depth}- Compare {left} vs {right}")
    if left < right:
        #print(f"{'  ' * (depth + 1)}- Left side is smaller, so inputs are in the right order")
        return True
    if left > right:
        #print(f"{'  ' * (depth + 1)}- Right side is smaller, so inputs are not in the right order")
        return False
    return None

def check_mixed_left(left: int, right: List[Any], depth: int = 1) -> Optional[bool]:
    #print(f"{'  ' * depth}- Compare {left} vs {right}")
    #print(f"{'  ' * (depth + 1)}- Mixed types; convert left to [{left}] and retry comparison")
    return check_list([left], right, depth + 1)

def check_mixed_right(left: List[Any], right: int, depth: int = 1) -> Optional[bool]:
    #print(f"{'  ' * depth}- Compare {left} vs {right}")
    #print(f"{'  ' * (depth + 1)}- Mixed types; convert right to [{right}] and retry comparison")
    return check_list(left, [right], depth + 1)

def check_list(left: List[Any], right: List[Any], depth: int = 0) -> Optional[bool]:
    #print(f"{'  ' * depth}- Compare {left} vs {right}")
    i = 0
    while i < max(len(left), len(right)):
        left_item = left[i] if i < len(left) else None
        right_item = right[i] if i < len(right) else None

        if left_item is None:
            #print(f"{'  ' * (depth + 1)}- Left side ran out of items, so inputs are in the right order")
            return True

        if right_item is None:
            #print(f"{'  ' * (depth + 1)}- Right side ran out of items, so inputs are not in the right order")
            return False

        if type(left_item) is list and type(right_item) is list:
            result = check_list(left_item, right_item, depth + 1)
            if result is not None:
                return result
            i += 1
        elif type(left_item) is int and type(right_item) is int:
            result = check_int(left_item, right_item, depth + 1)
            if result is not None:
                return result
            i += 1
        elif type(left_item) is int and type(right_item) is list:
            result = check_mixed_left(left_item, right_item, depth + 1)
            if result is not None:
                return result
            i += 1

        elif type(left_item) is list and type(right_item) is int:
            result = check_mixed_right(left_item, right_item, depth + 1)
            if result is not None:
                return result
            i += 1
        else:
            raise Exception(f"Unknown type {type(left_item)} {type(right_item)}")

def step_1():
    input = read_as_str_list(get_input_file())
    pairs_in_order = 0
    pair_index = 1
    for i in range(0, len(input) - 1, 3):
        packet_a = eval(input[i])
        packet_b = eval(input[i+1])
        result = check_list(packet_a, packet_b, 0)
        if result:
            pairs_in_order += pair_index
        pair_index += 1
    return pairs_in_order

def step_2():
    input = read_as_str_list(get_input_file())
    
    packets = []
    for row in input:
        if len(row) > 0:
            packets.append(eval(row))
    
    packets.append([[2]])
    packets.append([[6]])

    def sort_func(packet_a, packet_b) -> int:
        result = check_list(packet_a, packet_b, 0)
        if result == True:
            return -1
        if result is None:
            return 0
        return 1
    
    sorted_packets = sorted(packets, key=cmp_to_key(sort_func))
    divider_indices = []
    for i, packet in enumerate(sorted_packets):
        if packet == [[2]] or packet == [[6]]:
            divider_indices.append(i + 1)

    return divider_indices[0] * divider_indices[1]

if __name__ == '__main__':
    day = get_day_of_month()
    if is_test_run():
        assert step_1() == SOLUTION_1
        assert step_2() == SOLUTION_2
    else:
        print(f"---Day {day} / Part One---")
        print(step_1())
        print()
        print(f"---Day {day} / Part Two---")
        print(step_2())

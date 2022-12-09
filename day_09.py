from typing import Tuple
from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 6044
SOLUTION_2 = 2384

def is_touching(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> bool:
    if head_pos == tail_pos:
        return True

    x_diff = abs(head_pos[0] - tail_pos[0])
    y_diff = abs(head_pos[1] - tail_pos[1])

    return y_diff <= 1 and x_diff <= 1

def move_head(head_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    if direction == "U":
        return (head_pos[0], head_pos[1] + 1)
    if direction == "D":
        return (head_pos[0], head_pos[1] - 1)
    if direction == "R":
        return (head_pos[0] + 1, head_pos[1])
    
    return (head_pos[0] - 1, head_pos[1])

def move_tail(head_pos: Tuple[int, int], tail_pos: Tuple[int, int]) -> Tuple[int, int]:
    """Wow! Such beautiful mess! <3"""

    # Same column
    if head_pos[0] == tail_pos[0]:
        # Up
        if head_pos[1] > tail_pos[1]:
            return (tail_pos[0], tail_pos[1] + 1)
        # Down
        if head_pos[1] < tail_pos[1]:
            return (tail_pos[0], tail_pos[1] - 1)
    
    # Same row
    if head_pos[1] == tail_pos[1]:
        # Right
        if head_pos[0] > tail_pos[0]:
            return (tail_pos[0] + 1, tail_pos[1])
        # Left
        if head_pos[0] < tail_pos[0]:
            return (tail_pos[0] - 1, tail_pos[1])

    # Upper right
    if head_pos[0] > tail_pos[0] and head_pos[1] > tail_pos[1]:
        return (tail_pos[0] + 1, tail_pos[1] + 1)

    # Upper left
    if (head_pos[0] < tail_pos[0] and head_pos[1] > tail_pos[1]):
        return (tail_pos[0] - 1, tail_pos[1] + 1)

    # Lower right
    if (head_pos[0] > tail_pos[0] and head_pos[1] < tail_pos[1]):
        return (tail_pos[0] + 1, tail_pos[1] - 1)

    # Lower left
    if (head_pos[0] < tail_pos[0] and head_pos[1] < tail_pos[1]):
        return (tail_pos[0] - 1, tail_pos[1] - 1)

    raise Exception("Unknown case")

def step_1():
    steps = read_as_str_list(get_input_file())
    visited_positions = {"0,0": "#"}
    head_pos = (0, 0)
    tail_pos = (0, 0)

    for step in steps:
        if len(step) == 0:
            break
        direction, count = step.split(" ")
        count = int(count)
        
        for _ in range(0, count):
            head_pos = move_head(head_pos, direction)
            if is_touching(head_pos, tail_pos):
                continue

            tail_pos = move_tail(head_pos, tail_pos)
            key = f"{tail_pos[0]},{tail_pos[1]}"
            visited_positions[key] = "#"

    return len(visited_positions)
                


def step_2():
    steps = read_as_str_list(get_input_file())
    visited_positions = {"0,0": "#"}
    knot_pos = [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0), (0, 0)]

    for step in steps:
        if len(step) == 0:
            break
        direction, count = step.split(" ")
        count = int(count)
        
        for i in range(0, count):
            knot_pos[0] = move_head(knot_pos[0], direction)

            for i in range(1, len(knot_pos)):
                if is_touching(knot_pos[i-1], knot_pos[i]):
                    continue

                knot_pos[i] = move_tail(knot_pos[i-1], knot_pos[i])
                if (i == len(knot_pos) - 1):
                    key = f"{knot_pos[i][0]},{knot_pos[i][1]}"
                    visited_positions[key] = "#"

    return len(visited_positions)

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

from typing import Dict, List
from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run
import re

SOLUTION_1 = "SHQWSRBDL"
SOLUTION_2 = "CDTQZHBRS"

def step_1():
    rows = read_as_str_list(get_input_file())
    stacks: Dict[int, List[str]] = {}
    for row in rows:
        # Graph
        if "[" in row:
            columns = list(map(lambda r: r.replace("[", "").replace("]", "").strip(), re.findall("....", row + " ")))
            for i, col in enumerate(columns):
                if not i in stacks:
                    stacks[i] = []
                if col != "":
                    stacks[i].append(col)
        # Instruction
        elif "move" in row:
            parts = row.split(" ")
            number = int(parts[1])
            source = int(parts[3]) - 1
            target = int(parts[5]) - 1
            for i in range(0, number):
                crate = stacks[source].pop(0)
                stacks[target].insert(0, crate)

    top_crates = ""
    for stack in stacks.values():
        top_crates += stack[0]
    return top_crates

def step_2():
    rows = read_as_str_list(get_input_file())
    stacks: Dict[int, List[str]] = {}
    for row in rows:
        # Graph
        if "[" in row:
            columns = list(map(lambda r: r.replace("[", "").replace("]", "").strip(), re.findall("....", row + " ")))
            for i, col in enumerate(columns):
                if not i in stacks:
                    stacks[i] = []
                if col != "":
                    stacks[i].append(col)
        # Instruction
        elif "move" in row:
            parts = row.split(" ")
            number = int(parts[1])
            source = int(parts[3]) - 1
            target = int(parts[5]) - 1

            moving_stack = list(reversed(stacks[source][0: number]))
            del stacks[source][0:number]
            for i in range(0, len(moving_stack)):
                crate = moving_stack.pop(0)
                stacks[target].insert(0, crate)
                
    top_crates = ""
    for stack in stacks.values():
        top_crates += stack[0]
    return top_crates

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

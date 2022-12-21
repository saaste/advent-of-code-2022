from typing import Dict, Optional, Tuple
from utils.input import get_day_of_month, is_test_input, read_as_str, read_as_int_list, get_input_file, read_as_str_list
from utils.test import is_test_run
import time

SOLUTION_1 = 38914458159166
SOLUTION_2 = 3665520865940

class Monkey:
    name: str
    value: Optional[int] = None
    left: Optional["Monkey"] = None
    right: Optional["Monkey"] = None
    operator: Optional[str] = None

    def __init__(
        self,
        name: str,
        value: Optional[int] = None,
        left: Optional["Monkey"] = None,
        right: Optional["Monkey"] = None,
        operator: Optional[str] = None
    ) -> None:
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.operator = operator

    def __repr__(self) -> str:
        if self.value:
            return f"Monkey({self.name}, {self.value})"
        else:
            return f"Monkey({self.name}, {self.left} {self.operator} {self.right})"

def dfs(monkey: Monkey, monkeys: Dict[str, Monkey]) -> int:
    if monkey.value is not None:
        return monkey.value

    if monkey.left and monkey.right and monkey.operator:
        left = dfs(monkeys[monkey.left], monkeys)
        right = dfs(monkeys[monkey.right], monkeys)
        return eval(f"{left} {monkey.operator} {right}")

def dfs_2(monkey: Monkey, monkeys: Dict[str, Monkey], humn_value: int) -> Tuple[int, int]:
    if monkey.name == "humn":
        return humn_value
    
    if monkey.value is not None:
        return monkey.value

    if monkey.left and monkey.right and monkey.operator:
        left = dfs_2(monkeys[monkey.left], monkeys, humn_value)
        right = dfs_2(monkeys[monkey.right], monkeys, humn_value)
        if monkey.name == "root":
            return (left, right)
        else:
            return eval(f"{left} {monkey.operator} {right}")


def step_1():
    input = read_as_str_list(get_input_file())
    monkeys: Dict[str, Monkey] = {}
    for row in input:
        name, val = map(str.strip, row.split(":"))
        val_parts = val.split(" ")
        if len(val_parts) == 1:
            value = int(val_parts[0])
            monkeys[name] = Monkey(name=name, value=value)
        else:
            left, operator, right = val_parts
            monkeys[name] = Monkey(name=name, left=left, right=right, operator=operator)

    return int(dfs(monkeys["root"], monkeys))

def step_2():
    input = read_as_str_list(get_input_file())
    monkeys: Dict[str, Monkey] = {}
    for row in input:
        name, val = map(str.strip, row.split(":"))
        val_parts = val.split(" ")
        if len(val_parts) == 1:
            value = int(val_parts[0])
            monkeys[name] = Monkey(name=name, value=value)
        else:
            left, operator, right = val_parts
            monkeys[name] = Monkey(name=name, left=left, right=right, operator=operator)

    
    min = 0 if is_test_input() else -50000000000000
    max = 50000000000000
    while True:
        midpoint = (min + max) // 2
        
        left, right = dfs_2(monkeys["root"], monkeys, midpoint)
        if left == right:
            return midpoint

        if is_test_input():
            if left > right:
                max = midpoint
            else:
                min = midpoint
        else:
            if left < right:
                max = midpoint
            else:
                min = midpoint

        

if __name__ == '__main__':
    day = get_day_of_month()
    if is_test_run():
        assert step_1() == SOLUTION_1
        assert step_2() == SOLUTION_2
    else:
        
        print(f"---Day {day} / Part One---")
        start = time.time()
        print(step_1())
        mid = time.time()
        print(f"Runtime: {mid - start} seconds")
        print()
        print(f"---Day {day} / Part Two---")
        print(step_2())
        print(f"Runtime: {time.time() - mid} seconds")

from utils.input import (
    get_day_of_month,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run
import numpy as np

SOLUTION_1 = 466
SOLUTION_2 = 865


def step_1():
    pairs = read_as_str_list(get_input_file())
    fully_containing_pairs = 0
    for pair in pairs:
        if len(pair) == 0:
            break
        elfs = pair.split(",")
        elf_1 = list(map(int, elfs[0].split("-")))
        elf_2 = list(map(int, elfs[1].split("-")))

        if elf_1[0] <= elf_2[0] and elf_1[1] >= elf_2[1]:
            fully_containing_pairs += 1
            continue
        if elf_2[0] <= elf_1[0] and elf_2[1] >= elf_1[1]:
            fully_containing_pairs += 1
            continue

    return fully_containing_pairs


def step_2():
    pairs = read_as_str_list(get_input_file())
    overlapping_pairs = 0
    for pair in pairs:
        if len(pair) == 0:
            break

        elfs = pair.split(",")
        elf_1 = list(map(int, elfs[0].split("-")))
        elf_2 = list(map(int, elfs[1].split("-")))

        elf_1 = np.arange(elf_1[0], elf_1[1] + 1)
        elf_2 = np.arange(elf_2[0], elf_2[1] + 1)
        intersection = np.intersect1d(elf_1, elf_2)
        if len(intersection) > 0:
            overlapping_pairs += 1

    return overlapping_pairs


if __name__ == "__main__":
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

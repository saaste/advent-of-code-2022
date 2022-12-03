from utils.input import (
    get_day_of_month,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run

SOLUTION_1 = 8252
SOLUTION_2 = 2828

priorities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def step_1():
    rucksacks = read_as_str_list(get_input_file())
    sum = 0
    for rucksack in rucksacks:
        length = len(rucksack)

        if length == 0:
            break

        compartment_1 = rucksack[: length // 2]
        compartment_2 = rucksack[length // 2 :]

        uniq_items_1 = set(compartment_1)
        uniq_items_2 = set(compartment_2)

        duplicate_item = (uniq_items_1 & uniq_items_2).pop()
        sum += priorities.index(duplicate_item) + 1

    return sum


def step_2():
    rucksacks = read_as_str_list(get_input_file())
    sum = 0
    groups = len(rucksacks) // 3

    for i in range(groups):
        start_index = i * 3
        rucksack_1 = rucksacks[start_index]
        rucksack_2 = rucksacks[start_index + 1]
        rucksack_3 = rucksacks[start_index + 2]

        uniq_items_1 = set(rucksack_1)
        uniq_items_2 = set(rucksack_2)
        uniq_items_3 = set(rucksack_3)

        duplicate_item = (uniq_items_1 & uniq_items_2 & uniq_items_3).pop()
        sum += priorities.index(duplicate_item) + 1
    return sum


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

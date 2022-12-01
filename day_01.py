from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 72017
SOLUTION_2 = 212520

def step_1():
    input = read_as_str_list(get_input_file())
    elves = []
    elf_calories = 0
    for line in input:
        
        if len(line) > 0:
            elf_calories += int(line)
        else:
            elves.append(elf_calories)
            elf_calories = 0

    elves.append(elf_calories)
    elves.sort()
    elves.reverse()

    return elves[0]

def step_2():
    input = read_as_str_list(get_input_file())
    elves = []
    elf_calories = 0
    for line in input:
        
        if len(line) > 0:
            elf_calories += int(line)
        else:
            elves.append(elf_calories)
            elf_calories = 0

    elves.append(elf_calories)
    elves.sort()
    elves.reverse()

    return elves[0] + elves[1] + elves[2]

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

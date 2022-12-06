from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file
from utils.test import is_test_run

SOLUTION_1 = 1794
SOLUTION_2 = 2851


def step_1():
    message = read_as_str(get_input_file())
    for i in range(0, len(message)):
        test = message[i : i + 4]
        unique_chars = set(list(test))
        if len(unique_chars) == 4:
            return i + 4


def step_2():
    message = read_as_str(get_input_file())
    for i in range(0, len(message)):
        test = message[i : i + 14]
        unique_chars = set(list(test))
        if len(unique_chars) == 14:
            return i + 14


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

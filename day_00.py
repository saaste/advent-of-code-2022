from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file
from utils.test import is_test_run

SOLUTION_1 = ""
SOLUTION_2 = ""

def step_1():
    return read_as_str(get_input_file())

def step_2():
    return read_as_int_list(get_input_file())

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

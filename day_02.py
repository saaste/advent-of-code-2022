from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 13924
SOLUTION_2 = 13448

# ROCK = 1
# PAPER = 2
# SCISSORS = 3

opponent_map = {
    "A": 1,
    "B": 2,
    "C": 3,
}

my_map = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

def get_outcome_points(opponent_rps: int, my_rps: int) -> int:
    if opponent_rps == my_rps:
        return 3
    if my_rps == 3 and opponent_rps == 1:
        return 0
    if my_rps == 1 and opponent_rps == 3:
        return 6
    if my_rps > opponent_rps:
        return 6
    return 0

def get_win(opponent_rps: int) -> int:
    if opponent_rps == 3:
        return 1
    else:
        return opponent_rps + 1

def get_loose(opponent_rps: int) -> int:
    if opponent_rps == 1:
        return 3
    else:
        return opponent_rps - 1

def step_1():
    points = 0
    rounds = read_as_str_list(get_input_file())
    for round in rounds:
        rps = round.split(" ")
        opponent_rps = opponent_map.get(rps[0])
        my_rps = my_map.get(rps[1])
        round_points = get_outcome_points(opponent_rps, my_rps) + my_rps
        points += round_points

    return points

def step_2():
    points = 0
    rounds = read_as_str_list(get_input_file())
    for round in rounds:
        rps = round.split(" ")
        opponent_rps = opponent_map.get(rps[0])
        required_outcome = rps[1]
        my_rps = opponent_rps
        
        if required_outcome == "X":
            my_rps = get_loose(opponent_rps)
        elif required_outcome == "Z":
            my_rps = get_win(opponent_rps)

        round_points = get_outcome_points(opponent_rps, my_rps) + my_rps
        points += round_points
    return points

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

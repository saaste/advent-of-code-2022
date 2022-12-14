from typing import Dict, Tuple, Literal
from utils.input import (
    get_day_of_month,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run

SOLUTION_1 = 737
SOLUTION_2 = 28145


def build_cave(build_floor: bool = False) -> Dict[Tuple[int, int], str]:
    cave = {}
    scans = list(map(lambda x: x.split(" -> "), read_as_str_list(get_input_file())))
    for scan in scans:
        for i in range(0, len(scan) - 1):
            x, y = map(int, scan[i].split(","))
            x2, y2 = map(int, scan[i + 1].split(","))

            if x == x2:
                for j in range(min(y, y2), max(y, y2) + 1):
                    cave[(x, j)] = "#"
            else:
                for j in range(min(x, x2), max(x, x2) + 1):
                    cave[(j, y)] = "#"

    if build_floor:
        max_y = max(map(lambda x: x[1], cave.keys()))
        min_x = min(map(lambda x: x[0], cave.keys()))
        cave[(min_x, max_y + 2)] = "#"

    return cave


def drop_sand(
    cave: Dict[Tuple[int, int], str], max_y: int
) -> Tuple[Literal["added", "void"], Dict[Tuple[int, int], str]]:
    x = 500
    y = 0
    falling = True
    while falling:
        if y > max_y:
            falling = False
            return ("void", cave)
        elif (x, y + 1) not in cave:
            y += 1
        elif (x - 1, y + 1) not in cave:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in cave:
            x += 1
            y += 1
        else:
            cave[(x, y)] = "o"
            falling = False
            return ("added", cave)

    return cave


def drop_sand2(
    cave: Dict[Tuple[int, int], str], max_y: int
) -> Tuple[Literal["added", "void"], Dict[Tuple[int, int], str]]:
    x = 500
    y = 0
    falling = True
    while falling:
        if (500, 0) in cave:
            return ("void", cave)
        if (x, y + 1) not in cave and y + 1 < max_y:
            y += 1
        elif (x - 1, y + 1) not in cave and y + 1 < max_y:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in cave and y + 1 < max_y:
            x += 1
            y += 1
        else:
            cave[(x, y)] = "o"
            falling = False
            return ("added", cave)

    return cave


def step_1():
    cave = build_cave()
    max_y = max(map(lambda x: x[1], cave.keys()))
    sand_count = 0
    result = "added"
    while result == "added":
        sand_count += 1
        result, cave = drop_sand(cave, max_y)

    return sand_count - 1


def step_2():
    cave = build_cave(build_floor=True)
    max_y = max(map(lambda x: x[1], cave.keys()))
    sand_count = 0
    result = "added"
    while result == "added":
        sand_count += 1
        result, cave = drop_sand2(cave, max_y)

    return sand_count - 1


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

from typing import List
from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 1560
SOLUTION_2 = 252000

def build_forest() -> List[List[int]]:
    rows = read_as_str_list(get_input_file())
    tree = []
    for row in rows:
        if row == "":
            break
        tree.append(list(map(int, list(row))))
    return tree

def is_visible(forest, row, col) -> bool:
    length = len(forest)
    height = forest[row][col]

    # Edges are always visible
    if row == 0 or row == length -1 or col == 0 or col == length - 1:
        return True

    visible_from_top = True
    visible_from_bottom = True
    visible_from_left = True
    visible_from_right = True

    # Check top
    for i in range(row -1, -1, -1):
        if forest[i][col] >= height:
            visible_from_top = False
            break

    if visible_from_top:
        return True

    # Check bottom
    for i in range(row + 1, length):
        if forest[i][col] >= height:
            visible_from_bottom = False
            break

    if visible_from_bottom:
        return True

    # Check left
    for i in range(col - 1, -1, -1):
        if forest[row][i] >= height:
            visible_from_left = False
            break

    if visible_from_left:
        return True

    # Check right
    for i in range(col + 1, length):
        if forest[row][i] >= height:
            visible_from_right = False
            break

    if visible_from_right:
        return True

    return False

def calculate_scenic_score(forest, row, col) -> int:
    length = len(forest)
    height = forest[row][col]

    trees_top = 0
    trees_bottom = 0
    trees_left = 0
    trees_right = 0

    # Count top
    if row > 0:
        for i in range(row - 1, -1, -1):
            trees_top += 1
            if forest[i][col] >= height:
                break

    # Count bottom
    if row < length -1:
        for i in range(row + 1, length):
            trees_bottom += 1
            if forest[i][col] >= height:
                break

    # Count left
    if col > 0:
        for i in range(col - 1, -1, -1):
            trees_left += 1
            if forest[row][i] >= height:
                break

    # Count right
    if col < length - 1:
        for i in range(col +1, length):
            trees_right += 1
            if forest[row][i] >= height:
                break

    return trees_top * trees_bottom * trees_left * trees_right


def step_1():
    forest = build_forest()
    length = len(forest)
    
    # Outside border
    visible_trees = length  + (2 * (length - 1)) + length - 2
    for row, _ in enumerate(forest):
        if row == 0 or row == length - 1:
            continue

        for col, _ in enumerate(forest[row]):
            if col == 0 or col == length - 1:
                continue

            if is_visible(forest, row, col):
                visible_trees += 1

    return visible_trees

def step_2():
    forest = build_forest()
    max_scenic_score = 0
    for row, _ in enumerate(forest):
        for col, _ in enumerate(forest[row]):
            scenic_score = calculate_scenic_score(forest, row, col)
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score

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

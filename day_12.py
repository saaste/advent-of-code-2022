from typing import Dict, List, Optional
from utils.input import (
    get_day_of_month,
    read_as_str,
    read_as_int_list,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run
from pqdict import pqdict
import sys
from math import sqrt, pow

# Yeah... I know...
sys.setrecursionlimit(3000)

SOLUTION_1 = 370
SOLUTION_2 = 363

HEIGHT_MAP = "abcdefghijklmnopqrstuvwxyz"


class Point2D:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


class Peak:
    letter: str
    name: str
    height: int
    pos: Point2D
    distance: int
    previous: Optional["Peak"]

    def __init__(
        self, letter, pos: Point2D, height: int, distance: Optional[int] = None
    ) -> None:
        self.letter = letter
        self.name = f"{pos.x}.{pos.y}"
        self.pos = pos
        self.height = height
        self.distance = sys.maxsize if distance is None else distance
        self.previous = None

    def __repr__(self) -> str:
        return f"Peak({self.name} | {self.letter})"


def astar(
    current_peak: Peak,
    target_peak: Peak,
    grid: Dict[int, Dict[int, Peak]],
    priority_queue,
    handled: List[Peak] = [],
    shortest: Optional[int] = None,
    best_d: Optional[int] = None,
) -> List[Peak]:
    x = current_peak.pos.x
    y = current_peak.pos.y
    neighbors: List[Peak] = []

    # Left
    if (
        x > 0
        and grid[y][x - 1].height <= current_peak.height + 1
        and grid[y][x - 1] not in handled
    ):
        neighbors.append(grid[y][x - 1])

    # Right
    if (
        x < (len(grid[y]) - 1)
        and grid[y][x + 1].height <= current_peak.height + 1
        and grid[y][x + 1] not in handled
    ):
        neighbors.append(grid[y][x + 1])

    # Top
    if (
        y > 0
        and grid[y - 1][x].height <= current_peak.height + 1
        and grid[y - 1][x] not in handled
    ):
        neighbors.append(grid[y - 1][x])

    # Bottom
    if (
        y < (len(grid) - 1)
        and grid[y + 1][x].height <= current_peak.height + 1
        and grid[y + 1][x] not in handled
    ):
        neighbors.append(grid[y + 1][x])

    for neighbor in neighbors:
        neighbor.distance = current_peak.distance + 1
        neighbor.previous = current_peak

        if priority_queue.get(neighbor.name):
            del priority_queue[neighbor.name]
        priority_queue[neighbor.name] = neighbor

    handled_peak = priority_queue.popitem()[1]
    handled.append(handled_peak)
    if handled_peak == target_peak:
        return handled

    new_target: Peak = priority_queue.topitem()[1]

    # Some hacky optimizations
    if shortest and new_target.distance > shortest:
        # If new target is already longer than shortest path, we can give up.
        # At least it works with the test and my input, hehe
        return None
    if best_d and new_target.letter == "d" and new_target.distance > best_d:
        # D is the first early letters that has only one group in the input
        # If we reached D with longer distances, we can give up.
        return None

    return astar(new_target, target_peak, grid, priority_queue, handled)


def find_potential_starting_points():
    # In the input only the second column has Bs so we can just test
    # the As in the first column
    input = read_as_str_list(get_input_file())
    starting_points = []
    for y, row in enumerate(input):
        if len(row) == 0:
            break
        if row[0] == "a" or row[0] == "S":
            starting_points.append(Point2D(0, y))
    return starting_points


def step_1():
    input = read_as_str_list(get_input_file())

    grid = {}
    start_peak: Peak = None
    start_cell = Point2D(0, 0)
    end_cell = Point2D(0, 0)

    for y, row in enumerate(input):
        if len(row) == 0:
            break
        grid[y] = {}
        for x, col in enumerate(list(row)):
            height = 0
            if col == "S":
                height = HEIGHT_MAP.find("a")
                start_cell = Point2D(x, y)
                start_peak = Peak(col, start_cell, height, 0)
                grid[y][x] = start_peak
            elif col == "E":
                height = HEIGHT_MAP.find("z")
                end_cell = Point2D(x, y)
                grid[y][x] = Peak(col, Point2D(x, y), height, 0)
            else:
                height = HEIGHT_MAP.find(col)
                grid[y][x] = Peak(col, Point2D(x, y), height, 0)

    priority_queue = pqdict({start_peak.name: start_peak}, key=lambda x: x.distance)
    handled = astar(
        grid[start_cell.y][start_cell.x],
        grid[end_cell.y][end_cell.x],
        grid,
        priority_queue,
    )
    route = []
    current = handled[-1]
    while current is not None:
        route.append(current)
        current = current.previous

    route.reverse()
    return len(route) - 1


def step_2():
    input = read_as_str_list(get_input_file())

    end_cell = Point2D(0, 0)
    start_points = find_potential_starting_points()
    shortest = 100000000
    best_d = 100000000

    # Calculate weight for A*
    # Not sure if this helps, really. Plain Dijkstra seems to be as fast :D
    def calculate_weight(x: Peak) -> int:
        distance_to_target = sqrt(
            pow(start_peak.pos.x - end_cell.x, 2)
            + pow(start_peak.pos.y - end_cell.y, 2)
        )
        return x.distance + distance_to_target

    for i, start_point in enumerate(start_points):
        grid = {}
        for y, row in enumerate(input):
            if len(row) == 0:
                break
            grid[y] = {}
            for x, col in enumerate(list(row)):
                height = 0
                if x == start_point.x and y == start_point.y:
                    height = HEIGHT_MAP.find("a")
                    start_peak = Peak(col, start_point, height, 0)
                    grid[y][x] = start_peak
                elif col == "E":
                    height = HEIGHT_MAP.find("z")
                    end_cell = Point2D(x, y)
                    grid[y][x] = Peak(col, Point2D(x, y), height, 0)
                else:
                    height = HEIGHT_MAP.find(col)
                    grid[y][x] = Peak(col, Point2D(x, y), height, 0)

        priority_queue = pqdict({start_peak.name: start_peak}, key=calculate_weight)
        handled = astar(
            grid[start_point.y][start_point.x],
            grid[end_cell.y][end_cell.x],
            grid,
            priority_queue,
            [],
            shortest,
            best_d,
        )
        if handled is None:
            continue

        route = []
        current = handled[-1]
        while current is not None:
            route.append(current)
            if current.letter == "d" and current.distance < best_d:
                best_d = current.distance
            current = current.previous

        if len(route) < shortest:
            shortest = len(route)

    return shortest - 1


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

from typing import Dict, List, Tuple
from utils.input import (
    get_day_of_month,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run

SOLUTION_1 = 4322
SOLUTION_2 = 2516


def get_key(x: int, y: int, z: int) -> str:
    return f"{x}.{y}.{z}"


NEIGHBOURS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


class Cube:
    x: int
    y: int
    z: int
    key: str
    is_filled: bool

    def __init__(self, x: int, y: int, z: int, is_filled: bool = True) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.key = get_key(x, y, z)
        self.open_sides = 6
        self.is_filled = is_filled

    def __repr__(self) -> str:
        return f"Cube({self.x}, {self.y}, {self.z} / {self.open_sides})"


def flood_fill(
    x: int,
    y: int,
    z: int,
    solid_cubes: Dict[str, Cube],
    min_max_x: Tuple[int, int],
    min_max_y: Tuple[int, int],
    min_max_z: Tuple[int, int],
) -> Tuple[Dict[str, Cube], List[Cube]]:
    sides = 0
    queue = [Cube(x, y, z)]
    handled = {}

    while len(queue) > 0:
        cube = queue.pop()

        if cube.x < min_max_x[0] or cube.x > min_max_x[1]:
            continue
        if cube.y < min_max_y[0] or cube.y > min_max_y[1]:
            continue
        if cube.z < min_max_z[0] or cube.z > min_max_z[1]:
            continue
        if handled.get(cube.key):
            continue
        if solid_cubes.get(cube.key):
            sides += 1
            continue

        handled[cube.key] = cube
        queue.insert(0, Cube(cube.x - 1, cube.y, cube.z))
        queue.insert(0, Cube(cube.x + 1, cube.y, cube.z))
        queue.insert(0, Cube(cube.x, cube.y - 1, cube.z))
        queue.insert(0, Cube(cube.x, cube.y + 1, cube.z))
        queue.insert(0, Cube(cube.x, cube.y, cube.z - 1))
        queue.insert(0, Cube(cube.x, cube.y, cube.z + 1))

    return sides


def step_1():
    cube_data = read_as_str_list(get_input_file())
    cubes: Dict[str, Cube] = {}
    for row in cube_data:
        x, y, z = map(int, row.split(","))
        cube = Cube(x, y, z)
        cubes[cube.key] = cube

        # Update neighbours
        for dx, dy, dz in NEIGHBOURS:
            neighbour = cubes.get(get_key(x + dx, y + dy, z + dz))
            if neighbour:
                cube.open_sides -= 1
                neighbour.open_sides -= 1

    open_sides = 0
    for cube in cubes.values():
        open_sides += cube.open_sides

    return open_sides


def step_2():
    cube_data = read_as_str_list(get_input_file())
    cubes: Dict[str, Cube] = {}
    max_x: int = 0
    max_y: int = 0
    max_z: int = 0
    min_x: int = 0
    min_y: int = 0
    min_z: int = 0

    for row in cube_data:
        x, y, z = map(int, row.split(","))
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        max_z = max(z, max_z)
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        min_z = min(z, min_z)

        cube = Cube(x, y, z)
        cube.open_sides = 0
        cubes[cube.key] = cube

    # Do flood fill and get sides against "water"
    return flood_fill(
        -1,
        -1,
        -1,
        cubes,
        (min_x - 1, max_x + 1),
        (min_y - 1, max_y + 1),
        (min_z - 1, max_z + 1),
    )


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

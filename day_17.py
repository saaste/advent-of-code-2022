from typing import Dict, List, Optional, Tuple
from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file
from utils.test import is_test_run
from pqdict import pqdict
from copy import copy

SOLUTION_1 = 3175
SOLUTION_2 = ""  # 1574712641859 is too high, 1574712641858 is too high, 1574712643645 is too high, 1574712643613 is not right, 1574712643655 is not right


class Point2D:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


class Rock:
    type: int
    shape: Dict[str, Point2D]  # TODO Do we even need Point2D here?
    bottom_left: Point2D
    top_right: Point2D

    def __init__(self, type: int, shape: Dict[str, Point2D]) -> None:
        self.type = type
        self.shape = shape
        min_x = 1000000
        min_y = 1000000
        max_x = -1000000
        max_y = -1000000

        for point in shape.values():
            min_x = min(min_x, point.x)
            max_x = max(max_x, point.x)
            min_y = min(min_y, point.y)
            max_y = max(max_y, point.y)

        self.bottom_left = Point2D(min_x, min_y)
        self.top_right = Point2D(max_x, max_y)

    def move(self, vector: Point2D):
        new_shape: Dict[str, Point2D] = {}
        min_x = 1000000
        min_y = 1000000
        max_x = -1000000
        max_y = -1000000
        for point in self.shape.values():
            # Update shape
            new_x = point.x + vector.x
            new_y = point.y + vector.y
            new_shape[f"{new_x}.{new_y}"] = Point2D(new_x, new_y)

            min_x = min(min_x, new_x)
            max_x = max(max_x, new_x)
            min_y = min(min_y, new_y)
            max_y = max(max_y, new_y)

        # Update bounding box
        self.shape = new_shape
        self.bottom_left = Point2D(min_x, min_y)
        self.top_right = Point2D(max_x, max_y)

    def is_collision(self, point: Point2D) -> bool:
        # Check bounding box first
        if point.y > self.top_right.y:
            return False
        if point.x < self.bottom_left.x:
            return False
        if point.x > self.top_right.x:
            return False

        # Check shape to be more accurate
        for rock_point in self.shape.values():
            if point.x == rock_point.x and point.y == rock_point.y:
                return True

        return False


class Chamber:
    rocks: List[
        Rock
    ]  # TODO: Possible optimization. Priority queue based on Y value. Check highest rocks first
    bottom_left: Point2D
    top_right: Point2D
    top_row = [0, 1, 1, 1, 1, 1, 1, 1, 0]

    def __init__(self) -> None:
        self.rocks = []
        self.bottom_left = Point2D(0, 0)
        self.top_right = Point2D(8, 0)

    def add_rock(self, rock: Rock):
        self.rocks.insert(0, rock)
        self.bottom_left.x = min(self.bottom_left.x, rock.bottom_left.x)
        self.bottom_left.y = min(self.bottom_left.y, rock.bottom_left.y)
        self.top_right.x = max(self.top_right.x, rock.top_right.x)
        self.top_right.y = max(self.top_right.y, rock.top_right.y)

        new_top_row = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for point in rock.shape.values():
            if point.y == rock.top_right.y:
                new_top_row[point.x] = 1
        self.top_row = new_top_row

    def is_collision(self, rock: Rock) -> bool:
        # Left wall
        if rock.bottom_left.x == 0:
            return True

        # Right wall
        if rock.top_right.x == 8:
            return True

        # Floor
        if rock.bottom_left.y == 0:
            return True

        # Bounding box
        if rock.bottom_left.y > self.top_right.y:
            return False

        # Check each rock
        for stationary_rock in self.rocks:
            # Check bounding boxes
            if rock.bottom_left.y > stationary_rock.top_right.y:  # Above
                continue
            if rock.top_right.x < stationary_rock.bottom_left.x:  # Left
                continue
            if rock.bottom_left.x > stationary_rock.top_right.x:  # Right
                continue

            # Check each point (worst case scenario)
            for stationary_point in stationary_rock.shape.values():
                if rock.is_collision(stationary_point):
                    return True

        return False


class RockGenerator:
    next_type: int

    def __init__(self) -> None:
        self.next_type = 0

    def create_rock(self, y: int) -> Rock:
        if self.next_type == 0:
            self.next_type += 1
            return self.__create_horizontal(y)
        if self.next_type == 1:
            self.next_type += 1
            return self.__create_plus(y)
        if self.next_type == 2:
            self.next_type += 1
            return self.__create_corner(y)
        if self.next_type == 3:
            self.next_type += 1
            return self.__create_vertical(y)

        self.next_type = 0
        return self.__create_square(y)

    def __create_horizontal(self, y: int) -> Rock:
        y = y + 4
        shape: Dict[str, Point2D] = {}
        for x in range(3, 7):
            shape[f"{x}.{y}"] = Point2D(x, y)

        return Rock(0, shape)

    def __create_plus(self, y: int) -> Rock:
        y = y + 4
        shape = {
            f"4.{y+2}": Point2D(4, y + 2),  # top point
            f"3.{y+1}": Point2D(3, y + 1),  # left point
            f"4.{y+1}": Point2D(4, y + 1),  # center point
            f"5.{y+1}": Point2D(5, y + 1),  # right point
            f"4.{y}": Point2D(4, y),  # bottom point
        }
        return Rock(1, shape)

    def __create_corner(self, y: int) -> Rock:
        y = y + 4
        shape = {
            f"3.{y}": Point2D(3, y),
            f"4.{y}": Point2D(4, y),
            f"5.{y}": Point2D(5, y),
            f"5.{y+1}": Point2D(5, y + 1),
            f"5.{y+2}": Point2D(5, y + 2),
        }
        return Rock(2, shape)

    def __create_vertical(self, y: int) -> Rock:
        x = 3
        y += 4
        shape = {}
        for y in range(y, y + 4):
            shape[f"{x}.{y}"] = Point2D(x, y)
        return Rock(3, shape)

    def __create_square(self, y: int) -> Rock:
        y += 4
        shape = {
            f"3.{y}": Point2D(3, y),
            f"4.{y}": Point2D(4, y),
            f"3.{y+1}": Point2D(3, y + 1),
            f"4.{y+1}": Point2D(4, y + 1),
        }
        return Rock(4, shape)


def print_chamber(chamber: Chamber, falling_rock: Optional[Rock] = None):
    output = []

    # Borders
    falling_rock_y = falling_rock.top_right.y if falling_rock else 0
    for y in range(0, max(chamber.top_right.y + 1, falling_rock_y + 1)):
        row = ""
        for x in range(0, 9):
            if y > 0:
                if x == 0 or x == 8:
                    row += "|"
                else:
                    row += "."
            else:
                if x == 0 or x == 8:
                    row += "+"
                else:
                    row += "-"
        output.append(row)

    # Stationary rocks
    for rock in chamber.rocks:
        for point in rock.shape.values():
            value = output[point.y]
            value = value[: point.x] + "#" + value[point.x + 1 :]
            output[point.y] = value

    # Falling rocks
    if falling_rock:
        for point in falling_rock.shape.values():
            value = output[point.y]
            value = value[: point.x] + "@" + value[point.x + 1 :]
            output[point.y] = value

    output = "\n".join(reversed(output))
    print(output)
    print()


def step_1():
    wind_directions = read_as_str(get_input_file()).strip()
    chamber = Chamber()
    rock_generator = RockGenerator()

    wind_index = 0

    for i in range(0, 2022):
        # Create a new rock
        rock = rock_generator.create_rock(chamber.top_right.y)
        rock_falling = True

        # print_chamber(chamber, rock)
        while rock_falling:
            # Wind push
            push_vector = (
                Point2D(-1, 0) if wind_directions[wind_index] == "<" else Point2D(1, 0)
            )
            wind_index = wind_index + 1 if wind_index + 1 < len(wind_directions) else 0

            test_rock = copy(rock)
            test_rock.move(push_vector)
            if not chamber.is_collision(test_rock):
                rock = test_rock

            # print_chamber(chamber, rock)

            # Downward push
            push_vector = Point2D(0, -1)

            test_rock = copy(rock)
            test_rock.move(push_vector)
            if chamber.is_collision(test_rock):
                chamber.add_rock(rock)
                rock_falling = False
                # print_chamber(chamber)
            else:
                rock = test_rock
                # print_chamber(chamber, rock)

    return chamber.top_right.y


def step_2():
    pass


# def step_2():
#     wind_directions = read_as_str(get_input_file()).strip()
#     chamber = Chamber()
#     rock_generator = RockGenerator()

#     wind_index = 0
#     hashes = {}
#     rest_counter = None
#     full_cycles_height = None
#     height_at_cycle_found = None
#     height_at_initial_found = None

#     for rock_count in range(1, 11000):
#         if rest_counter is not None:
#             if rest_counter > 0:
#                 rest_counter -= 1
#             else:
#                 # print(
#                 #     f"Finished! Height is {full_cycles_height} + {chamber.top_right.y - height_at_cycle_found} - 2"
#                 # )
#                 return full_cycles_height + chamber.top_right.y

#         # Create a new rock
#         rock = rock_generator.create_rock(chamber.top_right.y)
#         rock_falling = True
#         hash = (
#             f"{str(rock.type)}+{str(wind_index)}+{''.join(map(str, chamber.top_row))}"
#         )
#         hash_value = hashes.get(hash, None)
#         if hash_value is not None and hash_value[2] >= 1 and rest_counter is None:
#             cycle_length = rock_count - hash_value[0]
#             cycle_height_increase = chamber.top_right.y - hash_value[1]

#             remaining_cycles = 1000000000000 - rock_count
#             full_cycles = remaining_cycles // cycle_length
#             full_cycles_height = full_cycles * cycle_height_increase

#             rest_counter = remaining_cycles - (full_cycles * cycle_length)
#             height_at_cycle_found = chamber.top_right.y
#             height_at_initial_found = hash_value[1]
#             print(f"Cycle detected on rock {rock_count}!")
#             print(
#                 f"Rock type: {rock.type}. Wind index: {wind_index}. Top row: {chamber.top_row}"
#             )
#             print(f"Full cycles: {full_cycles}")
#             print(
#                 f"Height increase of the cycle: {cycle_height_increase // hash_value[2]}"
#             )
#             print(f"Height of the stack: {chamber.top_right.y}")
#             print(f"Rest counter: {rest_counter}")
#             print(f"Same has appeared at {hashes.get(hash)}")
#         else:
#             if hash_value is None:
#                 hashes[hash] = (rock_count, chamber.top_right.y, 1)
#             else:
#                 hashes[hash] = (hash_value[0], hash_value[1], hash_value[2] + 1)

#         while rock_falling:
#             # Wind push
#             push_vector = (
#                 Point2D(-1, 0) if wind_directions[wind_index] == "<" else Point2D(1, 0)
#             )
#             if wind_index + 1 < len(wind_directions):
#                 wind_index += 1
#             else:
#                 wind_index = 0

#             # wind_index = wind_index + 1 if wind_index + 1 < len(wind_directions) else 0

#             test_rock = copy(rock)
#             test_rock.move(push_vector)
#             if not chamber.is_collision(test_rock):
#                 rock = test_rock

#             # print_chamber(chamber, rock)

#             # Downward push
#             push_vector = Point2D(0, -1)

#             test_rock = copy(rock)
#             test_rock.move(push_vector)
#             if chamber.is_collision(test_rock):
#                 previous_y = chamber.top_right.y
#                 chamber.add_rock(rock)
#                 new_y = chamber.top_right.y
#                 # print(f"Y increased {new_y - previous_y}")
#                 rock_falling = False
#                 # print_chamber(chamber)
#             else:
#                 rock = test_rock
#                 # print_chamber(chamber, rock)

#     # print_chamber(chamber)


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

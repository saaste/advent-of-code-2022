from typing import List, Dict, Optional, Tuple, Union
from utils.input import get_day_of_month, read_as_str, read_as_int_list, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 66292
SOLUTION_2 = 127012

Map = Dict[int, Dict[int, str]]

class Point2D():
    x: int
    y: int
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"

def parse_map(input: List[str]) -> Map:
    map: Dict[int, Dict[int, str]] = {}
    for row_idx, row in enumerate(input):
        if len(row.strip()) == 0:
            break

        row_dict: Dict[int, str] = {}
        for col_idx, char in enumerate(list(row)):
            row_dict[col_idx+1] = char
        map[row_idx+1] = row_dict
        

    return map

def parse_instructions(input: List[str]) -> List[Union[int, str]]:
    string = input[-1]
    instructions: List[Union[int, str]] = []
    collected_numbers = ""
    for i in range (0, len(string)):
        if not string[i].isnumeric():
            if len(collected_numbers) > 0:
                instructions.append(int(collected_numbers))
                collected_numbers = ""
            instructions.append(string[i])
        else:
            collected_numbers += string[i]

    if len(collected_numbers) > 0:
                instructions.append(int(collected_numbers))
    return instructions

def find_starting_point(map: Map) -> Point2D:
    for col, cell in map[1].items():
        if cell == ".":
            return Point2D(col, 1)

directions = ["R", "D", "L", "U"]
def turn(current_facing: str, instruction: str) -> str:
    if instruction == "L":
        index = (directions.index(current_facing) - 1) % len(directions)
    else:
        index = (directions.index(current_facing) + 1) % len(directions)
    return directions[index]

def take_step(current_position: Point2D, facing: str) -> Tuple[int, int]:
    vectors = {
        "R": Point2D(1, 0),
        "D": Point2D(0, 1),
        "L": Point2D(-1, 0),
        "U": Point2D(0, -1)
    }
    vector = vectors[facing]
    return Point2D(current_position.x + vector.x, current_position.y + vector.y)

def find_other_side(map: Map, position: Point2D, facing: str) -> Optional[Point2D]:
    if facing == "R":
        for x, cell in map[position.y].items():
            if cell == "#": # Wall on the other side, return current poisition
                return None
            if cell == ".":
                return Point2D(x, position.y)

    if facing == "L":
        cells: Tuple[int, str] = reversed(map[position.y].items())
        for x, cell in cells:
            if cell == "#": # Wall on the other side, return current poisition
                return None
            if cell == ".":
                return Point2D(x, position.y)

    if facing == "D":
        for y, row in map.items():
            cell = row[position.x]
            if cell == "#": # Wall on the other side, return current poisition
                return None
            if cell == ".":
                return Point2D(position.x, y)

    if facing == "U":
        rows = reversed(map.items())
        for y, row in rows:
            cell = row.get(position.x, "")
            if cell == "#": # Wall on the other side, return current poisition
                return None
            if cell == ".":
                return Point2D(position.x, y)


def figure_out_side(position: Point2D) -> int:
    if position.x <= 0 or position.y <= 0 or position.x > 150 and position.y > 200:
        raise Exception("Invalid position")

    if position.x >= 51 and position.x <= 100 and position.y <= 50:
        return 5
    if position.x >= 101 and position.y <= 50:
        return 6
    if position.x >= 51 and position.x <= 100 and position.y >= 51 and position.y <= 100:
        return 4
    if position.x >= 51 and position.x <= 100 and position.y >= 101 and position.y <= 150:
        return 3
    if position.x <= 50 and position.y >= 101 and position.y <= 150:
        return 2
    if position.x <= 50 and position.y >= 151:
        return 1
    raise Exception("Invalid position")

# I built a physical cube from paper and hard-coded each case
# Hey, if it works, it works! :D
def find_other_side_2(map: Map, position: Point2D, facing: str) -> Optional[Tuple[Point2D, str]]:
    side = figure_out_side(position)
    if side == 1:
        if facing == "L":
            new_x = 50 + (position.y - 150)
            new_y = 1
            new_facing = "D"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "R":
            new_x = 50 + (position.y - 150)
            new_y = 150
            new_facing = "U"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "D":
            new_x = 100 + position.x
            new_y = 1
            new_facing = "D"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
    if side == 2:
        if facing == "L":
            new_x = 51
            new_y = 51 - (position.y - 100)
            new_facing = "R"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "U":
            new_x = 51
            new_y = 50 + position.x
            new_facing = "R"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
    if side == 3:
        if facing == "R":
            new_x = 150
            new_y = 51 - (position.y - 100)
            new_facing = "L"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "D":
            new_x = 50
            new_y = 150 + (position.x - 50)
            new_facing = "L"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
    if side == 4:
        if facing == "L":
            new_x = position.y - 50
            new_y = 101
            new_facing = "D"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "R":
            new_x = 100 + (position.y - 50)
            new_y = 50
            new_facing = "U"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
    if side == 5:
        if facing == "L":
            new_x = 1
            new_y = 151 - position.y
            new_facing = "R"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "U":
            new_x = 1
            new_y = 150 + (position.x - 50)
            new_facing = "R"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
    if side == 6:
        if facing == "U":
            new_x = position.x - 100
            new_y = 200
            new_facing = "U"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "R":
            new_x = 100
            new_y = 151 - position.y
            new_facing = "L"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)
        if facing == "D":
            new_x = 100
            new_y = 50 + (position.x - 100)
            new_facing = "L"
            if map.get(new_y, {}).get(new_x, "") == ".":
                return (Point2D(new_x, new_y), new_facing)
            else:
                return (position, facing)

    raise Exception(f"Invalid case: {position} with facing {facing}")


def follow_move_instruction(map: Map, position: Point2D, instruction: int, facing: str, step: int = 1) -> Tuple[Point2D, str]:
    #print(f"Taking {instruction} steps")
    for i in range(instruction):
        new_position = take_step(position, facing)
        destination_cell = map.get(new_position.y, {}).get(new_position.x, "")
        if destination_cell == ".":
            position = new_position
            #print(f"Moved {facing} to {position}")
        elif destination_cell == "#":
            #print(f"Hit a wall in {position}")
            return (position, facing)
        else:
            # Figure out circular
            if step == 1:
                new_position = find_other_side(map, position, facing)
            else:
                new_position, new_facing = find_other_side_2(map, position, facing)
                facing = new_facing
            if new_position:
                position = new_position
            else:
                return (position, facing)
    return (position, facing)

def step_1():
    # Parse map and instructions
    map: Map = parse_map(read_as_str_list(get_input_file(), False))
    instructions = parse_instructions(read_as_str_list(get_input_file()))
    
    # Set starting point and facing
    position = find_starting_point(map)
    facing = "R"
    
    # Follow instructions
    for instruction in instructions:
        if isinstance(instruction, str):
            facing = turn(facing, instruction)
            #print(f"Turning {instruction}")
        else:
            position, _ = follow_move_instruction(map, position, instruction, facing)

    facing_map = {"R": 0, "D": 1, "L": 2, "U": 3}        
    return 1000 * position.y + 4 * position.x + facing_map[facing]
    
def step_2():
    # Parse map and instructions
    map: Map = parse_map(read_as_str_list(get_input_file(), False))
    instructions = parse_instructions(read_as_str_list(get_input_file()))

    # Set starting point and facing
    position = find_starting_point(map)
    facing = "R"
    
    # Follow instructions
    for instruction in instructions:
        if isinstance(instruction, str):
            facing = turn(facing, instruction)
            #print(f"Turning {instruction}")
        else:
            position, facing = follow_move_instruction(map, position, instruction, facing, 2)

    facing_map = {"R": 0, "D": 1, "L": 2, "U": 3}        
    return 1000 * position.y + 4 * position.x + facing_map[facing]

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

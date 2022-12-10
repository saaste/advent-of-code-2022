from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 13480
SOLUTION_2 = "####..##....##.###...##...##..####.#..#.\n#....#..#....#.#..#.#..#.#..#.#....#.#..\n###..#.......#.###..#....#....###..##...\n#....#.##....#.#..#.#.##.#....#....#.#..\n#....#..#.#..#.#..#.#..#.#..#.#....#.#..\n####..###..##..###...###..##..#....#..#."

def step_1():
    interesting_cycles = [20, 60, 100, 140, 180, 220]
    ops = read_as_str_list(get_input_file())
    cycle_num = 0
    x_register = 1
    signal_strengths = []

    for op in ops:
        if op == "":
            break
        parts = op.split(" ")
        if parts[0] == "noop":
            cycle_num += 1
            if cycle_num in interesting_cycles:
                signal_strengths.append(cycle_num * x_register)
        else:
            cycle_num += 1
            if cycle_num in interesting_cycles:
                signal_strengths.append(cycle_num * x_register)

            cycle_num += 1
            if cycle_num in interesting_cycles:
                signal_strengths.append(cycle_num * x_register)
            x_register += int(parts[1])
    
    return sum(signal_strengths)


def step_2():
    ops = read_as_str_list(get_input_file())
    cycle_num = 0
    x_register = 1
    pixel_pos = -1
    sprite_pos = [0, 1, 2]
    screen = ""
    
    def move_pixel(pixel_pos):
        if pixel_pos == 39:
            return 0
        return pixel_pos + 1

    def draw_pixel(pixel_pos, sprite_pos):
        value = "."
        if pixel_pos in sprite_pos:
            value = "#"
        if pixel_pos == 39:
            return f"{value}\n"
        return value

    for op in ops:
        if op == "":
            break
        parts = op.split(" ")
        if parts[0] == "noop":
            pixel_pos = move_pixel(pixel_pos)
            screen += draw_pixel(pixel_pos, sprite_pos)
            cycle_num += 1
            sprite_pos = [x_register - 1, x_register, x_register + 1]
        else:
            pixel_pos = move_pixel(pixel_pos)
            screen += draw_pixel(pixel_pos, sprite_pos)
            cycle_num += 1
            
            pixel_pos = move_pixel(pixel_pos)            
            screen += draw_pixel(pixel_pos, sprite_pos)
            x_register += int(parts[1])
            cycle_num += 1
            sprite_pos = [x_register - 1, x_register, x_register + 1]

    return screen.strip()
    

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

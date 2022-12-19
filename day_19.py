from random import random
from typing import List
from utils.input import (
    get_day_of_month,
    get_input_file,
    read_as_str_list,
)
from utils.test import is_test_run

SOLUTION_1 = 1487
SOLUTION_2 = 13440  # Finally got it by running randomizer long enough

# Correct values is 13440 {1: 17, 2: 40, 3: 21} so that I can optimize the
# code after finding the right answer. Still can take a long time :D


class Robot:
    ore_cost: int
    clay_cost: int
    obsidian_cost: int

    def __init__(
        self, ore_cost: int = 0, clay_cost: int = 0, obsidian_cost: int = 0
    ) -> None:
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost


class Blueprint:
    id: int
    ore_robot: Robot
    clay_robot: Robot
    obsidian_robot: Robot
    geode_robot: Robot

    def __init__(self, id: int) -> None:
        self.id = id


class Inventory:
    ore_bots: int = 1
    clay_bots: int = 0
    obsidian_bots: int = 0
    geode_bots: int = 0

    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


def simulate(blueprint: Blueprint, rounds: int, minutes: int) -> int:
    max_geode_amount: int = 0

    for _ in range(rounds):
        inventory = Inventory()
        for _ in range(1, minutes + 1):
            rnd = random()
            build_geode_robot = False
            build_obsidian_robot = False
            build_clay_robot = False
            build_ore_robot = False

            if (
                inventory.ore >= blueprint.geode_robot.ore_cost
                and inventory.obsidian >= blueprint.geode_robot.obsidian_cost
            ):
                build_geode_robot = True
                inventory.ore -= blueprint.geode_robot.ore_cost
                inventory.obsidian -= blueprint.geode_robot.obsidian_cost
            elif rnd <= 0.3 and inventory.ore >= blueprint.ore_robot.ore_cost:
                build_ore_robot = True
                inventory.ore -= blueprint.ore_robot.ore_cost
            elif (
                rnd <= 0.7
                and inventory.ore >= blueprint.obsidian_robot.ore_cost
                and inventory.clay >= blueprint.obsidian_robot.clay_cost
            ):
                build_obsidian_robot = True
                inventory.ore -= blueprint.obsidian_robot.ore_cost
                inventory.clay -= blueprint.obsidian_robot.clay_cost
            elif rnd <= 0.9 and inventory.ore >= blueprint.clay_robot.ore_cost:
                build_clay_robot = True
                inventory.ore -= blueprint.clay_robot.ore_cost
            else:
                pass

            inventory.ore += inventory.ore_bots
            inventory.clay += inventory.clay_bots
            inventory.obsidian += inventory.obsidian_bots
            inventory.geode += inventory.geode_bots

            if build_geode_robot:
                inventory.geode_bots += 1
            elif build_obsidian_robot:
                inventory.obsidian_bots += 1
            elif build_clay_robot:
                inventory.clay_bots += 1
            elif build_ore_robot:
                inventory.ore_bots += 1

        max_geode_amount = max(inventory.geode, max_geode_amount)

    return max_geode_amount


def step_1():
    ROUNDS = 500000
    input = read_as_str_list(get_input_file())
    blueprints: List[Blueprint] = []
    for row in input:
        parts = row.split(" ")

        blueprint = Blueprint(int(parts[1].replace(":", "")))
        blueprint.ore_robot = Robot(ore_cost=int(parts[6]))
        blueprint.clay_robot = Robot(ore_cost=int(parts[12]))
        blueprint.obsidian_robot = Robot(
            ore_cost=int(parts[18]), clay_cost=int(parts[21])
        )
        blueprint.geode_robot = Robot(
            ore_cost=int(parts[27]), obsidian_cost=int(parts[30])
        )
        blueprints.append(blueprint)

    quality_levels = {}
    for blueprint in blueprints:
        max_geode_amount = simulate(blueprint, ROUNDS, 24)
        quality_levels[blueprint.id] = max_geode_amount

    print(f"Quality levels: {quality_levels}")

    result = 0
    for id, quality_level in quality_levels.items():
        result += id * quality_level
    return result


def step_2():
    input = read_as_str_list(get_input_file())
    blueprints: List[Blueprint] = []
    for row in input:
        parts = row.split(" ")

        blueprint = Blueprint(int(parts[1].replace(":", "")))
        blueprint.ore_robot = Robot(ore_cost=int(parts[6]))
        blueprint.clay_robot = Robot(ore_cost=int(parts[12]))
        blueprint.obsidian_robot = Robot(
            ore_cost=int(parts[18]), clay_cost=int(parts[21])
        )
        blueprint.geode_robot = Robot(
            ore_cost=int(parts[27]), obsidian_cost=int(parts[30])
        )
        blueprints.append(blueprint)

    quality_levels = {}
    correct_answers = {
        1: 16,
        2: 40,
        3: 21,
    }
    for blueprint in blueprints[:3]:
        best_result = 0
        run = 1
        while best_result < correct_answers[blueprint.id]:
            max_geode_amount = simulate(blueprint, 1000000, 32)
            best_result = max(max_geode_amount, best_result)
            quality_levels[blueprint.id] = best_result
            run += 1
            print(
                f"Run {run * 1000000} for blueprint {blueprint.id}. Best result: {best_result} / {correct_answers[blueprint.id]}"
            )

    print(f"Quality levels: {quality_levels}")

    result = 1
    for quality_level in quality_levels.values():
        result *= quality_level
    return result


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

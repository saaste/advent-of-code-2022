from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 110264
SOLUTION_2 = 23612457316

def parse_rules():
    rows = read_as_str_list(get_input_file())
    monkeys = {}
    monkey_id = 0

    for row in rows:
        row = row.replace("  ", "")
        if len(row) == 0:
            continue

        parts = row.split(" ")
        if parts[0].startswith("Monkey"):
            monkey_id = int(parts[1].replace(":", ""))
            monkeys[monkey_id] = {"id": monkey_id, "inspections": 0}
        elif parts[0].startswith("Starting"):
            items = row.replace("Starting items: ", "").replace(",", "").strip()
            items = list(map(lambda x: int(x), items.split(" ")))
            monkeys[monkey_id]["items"] = items
        elif parts[0].startswith("Operation"):
            op = parts[4]
            op_target = parts[5]
            monkeys[monkey_id]["op"] = f"{op} {op_target}"
        elif parts[0].startswith("Test"):
            divisible = int(parts[3])
            monkeys[monkey_id]["test"] = divisible
        elif parts[1].startswith("true"):
            true_target = int(parts[5])
            monkeys[monkey_id]["true_target"] = true_target
        elif parts[1].startswith("false"):
            false_target = int(parts[5])
            monkeys[monkey_id]["false_target"] = false_target
        else:
            raise Exception(f"Parse failed: {row}")

    return monkeys

def play_with_monkies(rounds: int, make_smaller: bool) -> int:
    monkeys = parse_rules()

    prime_divisors = list(map(lambda x: x["test"], monkeys.values()))
    prime_product = 1
    for divisor in prime_divisors:
        prime_product = prime_product * divisor

    for _ in range(0, rounds):
        for id, info in monkeys.items():
            op, rule_target = info["op"].split(" ")
            for item in info["items"]:
                monkeys[id]["inspections"] += 1                
                
                if (rule_target == "old"):
                    target = item
                else:
                    target = int(rule_target)

                if op == "+":
                    item = item + target
                else:
                    item = item * target

                if make_smaller:
                    item = item % prime_product
                else:
                    item = item // 3

                if item % info["test"] == 0:
                    monkeys[info["true_target"]]["items"].append(item)
                else:
                    monkeys[info["false_target"]]["items"].append(item)
                
                monkeys[id]["items"] = []

    monkeys = list(monkeys.values())
    monkeys = sorted(monkeys, key=lambda x: x["inspections"])
    monkeys.reverse()
    return monkeys[0]["inspections"] * monkeys[1]["inspections"]

def step_1():
    return play_with_monkies(20, False)

def step_2():
    return play_with_monkies(10000, True)

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

from typing import List, Optional
from utils.input import get_day_of_month, read_as_int_list, get_input_file
from utils.test import is_test_run

SOLUTION_1 = 988
SOLUTION_2 = 7768531372516

class Node():
    number: int
    left: Optional["Node"]
    right: Optional["Node"]

    def __init__(self, number: int, left: Optional["Node"] = None, right: Optional["Node"] = None) -> None:
        self.number = number
        self.left = left
        self.right = right

    def move_right(self, n: int):
        if n == 0:
            return

        for _ in range(n):
            old_left = self.left
            new_left = self.right
            new_right = self.right.right

            self.left = new_left
            self.right = new_right
            self.left.left = old_left
            self.left.right = self
            self.right.left = self

            old_left.right = self.left

    def move_left(self, n: int):
        if n == 0:
            return
        for _ in range(n):
            old_right = self.right
            new_left = self.left.left
            new_right = self.left

            self.left = new_left
            self.right = new_right
            self.right.right = old_right
            self.left.right = self
            self.right.left = self

            old_right.left = self.right

    def traverse_right(self, n):
        if n <= 0:
            raise Exception("Nope!")

        right = self.right
        for i in range(n - 1):
            right = right.right

        return right


    def __repr__(self) -> str:
        return str(self.number)    

def step_1():
    numbers: List[int] = read_as_int_list(get_input_file())
    nodes: List[Node] = []
    zero_node: Node = None
    node_count = len(numbers)
    for index, number in enumerate(numbers):
        if index == 0:
            node = Node(number)
            nodes.append(node)
        elif index == len(numbers) - 1:
            node = Node(number, nodes[index - 1], nodes[0])
            nodes.append(node)
            nodes[index -1].right = node
            nodes[0].left = node
        else:
            node = Node(number, nodes[index - 1])
            nodes.append(node)
            nodes[index -1].right = node

        if number == 0:
            zero_node = node
    
    for node in nodes:
        node_move = abs(node.number)
        if node_move > node_count:
             node_move = (node_move % node_count) + 1

        if node.number == 0 or node_move == 0:
            continue

        if node.number > 0:
            node.move_right(node_move)
        elif node.number < 0:
            node.move_left(node_move)

    result_numbers = [zero_node.traverse_right(1000).number, zero_node.traverse_right(2000).number, zero_node.traverse_right(3000).number]
    return sum(result_numbers)

def step_2():
    numbers: List[int] = read_as_int_list(get_input_file())
    nodes: List[Node] = []
    zero_node: Node = None
    node_count = len(numbers)
    for index, number in enumerate(numbers):
        number *= 811589153
        if index == 0:
            node = Node(number)
            nodes.append(node)
        elif index == len(numbers) - 1:
            node = Node(number, nodes[index - 1], nodes[0])
            nodes.append(node)
            nodes[index -1].right = node
            nodes[0].left = node
        else:
            node = Node(number, nodes[index - 1])
            nodes.append(node)
            nodes[index -1].right = node

        if number == 0:
            zero_node = node
        
    for i in range(10):
        print(f"Round {i}")
        for node in nodes:
            
            node_move = abs(node.number)
            if node_move >= node_count:
                node_move = node_move % (node_count - 1)

            if node.number == 0 or node_move == 0:
                continue

            if node.number > 0:
                node.move_right(node_move)
            elif node.number < 0:
                node.move_left(node_move)

    result_numbers = [zero_node.traverse_right(1000 % node_count).number, zero_node.traverse_right(2000 % node_count).number, zero_node.traverse_right(3000 % node_count).number]
    print(result_numbers)
    return sum(result_numbers)

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

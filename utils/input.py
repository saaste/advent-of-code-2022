import sys
from typing import List
import os

def get_day_of_month() -> str:
    return sys.argv[0][4:6]

def get_input_file() -> str:
    script_file = os.path.basename(sys.argv[0])
    if "--test-input" in sys.argv:
        return f"inputs/{script_file.replace('.py', '.test.txt')}"
    
    return f"inputs/{script_file.replace('.py', '.txt')}"

def read_as_str(path: str) -> str:
    with open(path) as f:
        content = f.read()
    return content

def read_as_str_list(path: str) -> List[str]:
    return read_as_str(path).split("\n")

def read_as_int_list(path: str) -> List[int]:
    return list(map(lambda str: int(str), read_as_str_list(path)))
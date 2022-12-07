from typing import Dict, Literal, Optional, List
from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 1581595
SOLUTION_2 = 1544176

DISK_SPACE = 70000000
SPACE_NEEDED = 30000000

class Directory():
    name: str
    subdirs: Dict[str, "Directory"]
    files: Dict[str, int]
    parent: Optional["Directory"]
    size: int

    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self.name = name
        self.files = {}
        self.subdirs = {}
        self.parent = parent
        self.size = 0

    def add_file(self, filename: str, file_size: int):
        self.files[filename] = file_size
        self.size += file_size
        if self.parent:
            self.parent._add_size(file_size)

    def _add_size(self, size: int):
        self.size += size
        if self.parent:
            self.parent._add_size(size)

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name

def collect_directories() -> Directory:
    lines = read_as_str_list(get_input_file())
    current_dir = None

    for line in lines:
        if len(line) == 0:
            break
        
        if line.startswith("$ cd"):
            dir_name = line.split(" ")[2]
            if dir_name == "..":
                current_dir = current_dir.parent
            else:
                if not current_dir:
                    current_dir = Directory(dir_name)
                else:
                    current_dir = current_dir.subdirs[dir_name]
        elif line.startswith("$ ls"):
            pass
        elif line.startswith("dir "):
            dir_name = line.split(" ")[1]
            current_dir.subdirs[dir_name] = Directory(dir_name, current_dir)
            pass
        else:
            (size, filename) = line.split(" ")
            current_dir.add_file(filename, int(size))

    while current_dir.parent is not None:
        current_dir = current_dir.parent
    
    return current_dir

def collect_dirs_of_size(current_directory: Directory, limit: int, op: Literal["gte","lte"], matching_dirs: List[Directory]) -> List[Directory]:
    if op == "lte" and current_directory.size <= limit:
        matching_dirs.append(current_directory)
    elif op == "gte" and current_directory.size >= limit:
        matching_dirs.append(current_directory)


    if len(current_directory.subdirs) > 0:
        for subdir in current_directory.subdirs.values():
            matching_dirs += collect_dirs_of_size(subdir, limit, op, matching_dirs)

    return list(set(matching_dirs))

def step_1():
    current_dir = collect_directories()
    matching_dirs = collect_dirs_of_size(current_dir, 100000, "lte", [])
    total_sum = sum(list(map(lambda d: d.size, matching_dirs)))
    return total_sum

def step_2():
    current_dir = collect_directories()
    deletion_needed = SPACE_NEEDED - (DISK_SPACE - current_dir.size)
    matching_dirs = collect_dirs_of_size(current_dir, deletion_needed, "gte", [])

    directory_to_be_deleted = None
    for dir in matching_dirs:
        if directory_to_be_deleted is None:
            directory_to_be_deleted = dir
        elif dir.size < directory_to_be_deleted.size:
            directory_to_be_deleted = dir
    return directory_to_be_deleted.size

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

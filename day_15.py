from typing import List, Optional, Tuple
from utils.input import get_day_of_month, get_input_file, read_as_str_list
from utils.test import is_test_run

SOLUTION_1 = 5299855
SOLUTION_2 = 13615843289729

class Point2D:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"

class Sensor:
    pos: Point2D
    closest_beacon_pos: Point2D
    manhattan_distance: int

    def __init__(self, x, y, beacon_x, beacon_y) -> None:
        self.pos = Point2D(x, y)
        self.closest_beacon_pos = Point2D(beacon_x, beacon_y)
        self.manhattan_distance = abs(x - beacon_x) + abs(y - beacon_y)

    def is_inside_scan_area(self, point: Point2D) -> bool:
        scanner_y = abs(self.pos.y)
        point_y = abs(point.y)
        diff = max(scanner_y, point_y) - min(scanner_y, point_y)
        
        if diff > self.manhattan_distance:
            return False

        distance_at_y = self.manhattan_distance - diff
        if distance_at_y < 0:
            return False
        
        min_x_at_pos = self.pos.x - distance_at_y
        max_x_at_pos = self.pos.x + distance_at_y

        return min_x_at_pos <= point.x and point.x >= max_x_at_pos

    def checked_points_on_row(self, row: int) -> Optional[Tuple[int, int]]:
        scanner_y = abs(self.pos.y)
        diff = max(scanner_y, row) - min(scanner_y, row)

        if diff > self.manhattan_distance:
            return None

        distance_at_y = self.manhattan_distance - diff
        if distance_at_y < 0:
            return None

        min_x_at_pos = self.pos.x - distance_at_y
        max_x_at_pos = self.pos.x + distance_at_y

        return (min_x_at_pos, max_x_at_pos)


    def __repr__(self) -> str:
        return f"Sensor({self.pos}, {self.closest_beacon_pos}, {self.scan_area})"

def expand_checked_areas(checked_areas: List[Tuple[int, int]], sensor_area: Tuple[int, int]) -> List[Tuple[int, int]]:
    if len(checked_areas) == 0:
        checked_areas.append(sensor_area)
        return checked_areas

    sensor_min, sensor_max = sensor_area
    for i in range(0, len(checked_areas)):
        area_min, area_max = checked_areas[i]
        
        # Sensor is inside existing area, skip
        if sensor_min >= area_min and sensor_max <= area_max:
            return checked_areas

        # Sensor covers existing area, replace
        if sensor_min < area_min and sensor_max > area_max:
            checked_areas[i] = sensor_area
            return checked_areas

        # Sensor min is more left, expand
        if sensor_min < area_min and sensor_max >= area_min and sensor_max <= area_max:
            checked_areas[i] = (sensor_min, area_max)
            return checked_areas

        # sensor max is more right, expand
        if sensor_max > area_max and sensor_min >= area_min and sensor_min <= area_max:
            checked_areas[i] = (area_min, sensor_max)
            return checked_areas

    # Not overlapping, add new
    checked_areas.append(sensor_area)
    return checked_areas
    

def step_1(y: int):
    readings = read_as_str_list(get_input_file())
    sensors: List[Sensor] = []
    for reading in readings:
        sensor, beacon = reading.split(": ")
        sensor_parts = sensor.split(" ")
        sensor_x = int(sensor_parts[2].replace("x=", "").replace(",", ""))
        sensor_y = int(sensor_parts[3].replace("y=", ""))
        beacon_parts = beacon.split(" ")
        beacon_x = int(beacon_parts[4].replace("x=", "").replace(",", ""))
        beacon_y = int(beacon_parts[5].replace("y=", ""))
        sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(sensor)

    sensor_areas: List[Tuple[int, int]] = []
    checked_areas: List[Tuple[int, int]] = []
    
    for sensor in sensors:
        sensor_area = sensor.checked_points_on_row(y)
        if sensor_area:
            sensor_areas.append(sensor_area)
    sensor_areas = sorted(sensor_areas, key=lambda area: area[0])


    checked_areas = []
    for sensor_area in sensor_areas:
        checked_areas = expand_checked_areas(checked_areas, sensor_area)

    return checked_areas[0][1] - checked_areas[0][0]            


def step_2(max_coordinate: int):
    readings = read_as_str_list(get_input_file())
    sensors: List[Sensor] = []
    for reading in readings:
        sensor, beacon = reading.split(": ")
        sensor_parts = sensor.split(" ")
        sensor_x = int(sensor_parts[2].replace("x=", "").replace(",", ""))
        sensor_y = int(sensor_parts[3].replace("y=", ""))
        beacon_parts = beacon.split(" ")
        beacon_x = int(beacon_parts[4].replace("x=", "").replace(",", ""))
        beacon_y = int(beacon_parts[5].replace("y=", ""))
        sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(sensor)
    
    # Awwwyah, brute force all 4 000 000 rows!
    # Takes about 1 minute on my machine, but I'll take it!
    for y in range(0, max_coordinate + 1):
        sensor_areas: List[Tuple[int, int]] = []
        checked_areas: List[Tuple[int, int]] = []
        for sensor in sensors:
            sensor_area = sensor.checked_points_on_row(y)
            if sensor_area:
                sensor_areas.append(sensor_area)
        sensor_areas = sorted(sensor_areas, key=lambda area: area[0])

        for sensor_area in sensor_areas:
            checked_areas = expand_checked_areas(checked_areas, sensor_area)
        
        if len(checked_areas) == 2 and checked_areas[1][0] - checked_areas[0][1] == 2:
            x = checked_areas[0][1] + 1
            return x * 4000000 + y

if __name__ == '__main__':
    day = get_day_of_month()
    if is_test_run():
        assert step_1(2000000) == SOLUTION_1
        assert step_2(4000000) == SOLUTION_2
    else:
        print(f"---Day {day} / Part One---")
        print(step_1(2000000))
        print()
        print(f"---Day {day} / Part Two---")
        print(step_2(4000000))

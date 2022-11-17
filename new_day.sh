#!/bin/sh
current_day=$(date '+%d')
cp inputs/day_00.txt "inputs/day_$current_day.txt"
cp inputs/day_00.test.txt "inputs/day_$current_day.test.txt"
cp day_00.py "day_$current_day.py"
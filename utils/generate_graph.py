#!/usr/bin/python3
# Dot graph generator
import decomptable_util
import csv
import sys


table = []

if len(sys.argv) < 2:
    print(f'{sys.argv[0]} decomptable(.csv | .bin)')
    exit()

if sys.argv[1].endswith('.csv'):
    with open(sys.argv[1], newline='') as f:
        table = decomptable_util.from_csv(csv.reader(f))
else:
    with open(sys.argv[1], 'rb') as f:
        table = decomptable_util.unpack(f.read())

COLOR = 0
UNKSHORT = 1
UNKBOOL = 2
JUMP = 3

ARROW_0 = "[arrowhead=onormal]"
ARROW_1 = "[arrowhead=normal]"

COLOR_RED = "[color=red]"
COLOR_BLACK = "[color=black]"

print("digraph table {")
print('    start8 -> 0')
print('    start16 -> 8')
for n, i in enumerate(table):
    if n != i[0][JUMP] and i[0][JUMP] != 511:
        label = f'[label={i[0][UNKSHORT]}]' if i[0][UNKSHORT] > 0 else ''
        print(f'    {n} -> {i[0][JUMP] if i[0][JUMP] != 0 else "end"} ' +
              f'{ARROW_0}{COLOR_RED if i[0][UNKBOOL] else COLOR_BLACK}{label};')
    if n != i[1][JUMP] and i[1][JUMP] != 511:
        label = f'[label={i[1][UNKSHORT]}]' if i[1][UNKSHORT] > 0 else ''
        print(f'    {n} -> {i[1][JUMP] if i[1][JUMP] != 0 else "end"} ' +
              f'{ARROW_1}{COLOR_RED if i[1][UNKBOOL] else COLOR_BLACK}{label};')
print("}")

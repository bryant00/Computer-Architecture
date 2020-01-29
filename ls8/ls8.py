#!/usr/bin/env python3
import argparse

"""Main."""

# python3 ls8.py examples/mult.ls8

"""python
sys.argv[0] == "ls8.py"
sys.argv[1] == "examples/mult.ls8"
"""

import sys
from cpu import *

parser = argparse.ArgumentParser()
parser.add_argument("file", help="ops filename")
args = parser.parse_args()
filename = args.file


# with open(filename, "rb") as f:
#     read_data = f.read()
# print(read_data)

from functools import partial

cpu = CPU()
blocks = []
with open(filename, "r") as f:
    # for block in iter(partial(f.read, 8), b""):
    # for row in f:
    #     split = row.split("#")
    #     rom = split[0]
    #     if rom == "":
    #         continue
    #     else:
    #         print(partial(rom, 8))
    #         # if not row or row.startswith(b"#"):
    #         #     blocks.append([])
    #         # for block in iter(partial(rom, 8), b""):
    #         blocks.append(rom)
    for line in f:
        comment_split = line.split("#")  # used to ignore comments
        instruction = comment_split[0]
        if instruction == "":
            continue
        else:
            blocks.append(instruction[:8])

# print(blocks)
cpu.load(blocks)
cpu.run()

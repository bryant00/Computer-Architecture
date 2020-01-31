import sys
from cpu import *

filename = sys.argv[1]
# print(filename)

cpu = CPU()

cpu.load()
cpu.run()

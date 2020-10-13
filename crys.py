#!/usr/bin/python3
# Cryptarithm solver using DFS
# Bart Massey

import sys

# Read in a cryptarithm.
class Puzzle(object):
    
    def __init__(self, f):

        # Read in a line and split into characters.
        def read_line():
            line = next(f).strip()
            return [c for c in line]

        self.lines = [read_line() for _ in range(3)]
        vars = set()
        for line in self.lines:
            vars |= set(line)
        self.vars = list(vars)
        self.vals = dict()
    
    def show(self):
        max_width = max([len(l) for l in self.lines])
        for l in self.lines:
            width = len(l)
            for _ in range(max_width - width):
                print(" ", end="")
            for c in l:
                if c in self.vals:
                    print(self.vals[c], end="")
                else:
                    print(c, end="")
            print()

puzzle = Puzzle(open(sys.argv[1], "r"))
puzzle.vals["s"] = 1
puzzle.show()

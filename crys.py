#!/usr/bin/python3
# Cryptarithm solver using DFS
# Bart Massey

import sys

DEBUG = True
def debug(*args, enable=True):
    if DEBUG and enable:
        print(*args)

# Read in a cryptarithm.
class Puzzle(object):
    
    def __init__(self, f):

        # Read in a line and split into characters.
        def read_line():
            while True:
                line = next(f)
                if line and line[0] != "#":
                    break
            line = line.strip()
            return [c for c in line]

        # Read the three instance lines.
        lines = [read_line() for _ in range(3)]

        # Normalize the line lengths by padding with "letter" 0.
        max_width = max([len(l) for l in lines])
        self.lines = [ ["0"] * (max_width - len(l)) + l for l in lines ]

        # Order the variables right-to-left top-to-bottom.
        # XXX vars is a Python built-in, so pvars.
        pvars = []
        for j in reversed(range(max_width)):
            for i in range(3):
                c = self.lines[i][j]
                if c == "0" or c in pvars:
                    continue
                pvars.append(c)
        self.pvars = pvars

        # List of tuples forming the columns of the equation.
        l = self.lines
        tuples = [(l[0][i], l[1][i], l[2][i]) for i in range(max_width)]
        self.tuples = list(tuples)
    
        # List of variables that lead the terms.
        leading = set()
        for (i, line) in enumerate(self.lines):
            for c in line:
                if c != "0":
                    leading.add(c)
                    break
        self.leading = list(leading)

    # Print out a puzzle with solved variables substituted.
    def show(self, vals=dict()):
        for l in self.lines:
            for c in l:
                if c == "0":
                    print(" ", end="")
                elif c in vals:
                    n = len(vals[c])
                    if n == 0:
                        print("-", end="")
                    elif n == 1:
                        print(set(vals[c]).pop(), end="")
                    else:
                        print("*", end="")
                else:
                    print(c, end="")
            print()

    # Solve a cryptarithm. Strategy: depth-first search with
    # variables ordered right-to-left and lowest values
    # tried first.
    def solve(self):

        def extend(tuples, ranges, carry):
            # Base case: All tuples cleared.
            if not tuples:
                if carry == 0:
                    return dict(ranges)
                return None

            # Recursive case: Value current tuple and
            # extend.
            ts = list(tuples)
            t = ts.pop()
            v1 = t[0]
            v2 = t[1]
            s = t[2]
            for v1d in ranges[v1]:
                for v2d in ranges[v2]:
                    ss = v1d + v2d + carry
                    sd = ss
                    sc = 0
                    if sd >= 10:
                        sd -= 10
                        sc = 1
                    if sd in ranges[s]:
                        rs = { k : set(ranges[k]) for k in ranges }
                        rs[v1] = {v1d}
                        rs[v2] = {v2d}
                        rs[s] = {sd}

                        def stopped(vv, vd):
                            if vv == '0':
                                return False
                            for v in rs:
                                if v == '0' or v == vv:
                                    continue
                                rs[v] -= {vd}
                                if not rs[v]:
                                    return True
                            return False

                        if (stopped(v1, v1d) or
                            stopped(v2, v2d) or
                            stopped(s, sd)):
                            continue

                        result = extend(ts, rs, sc)
                        if result is not None:
                            return result

            # Could not find an extension.
            return None

        start_tuples = list(self.tuples)
        start_ranges = { pvar: set(range(10)) for pvar in self.pvars }
        start_ranges['0'] = {0}
        for v in self.leading:
            start_ranges[v] -= {0}
        if start_tuples[0][0] == '0':
            assert start_tuples[0][1] == '0'
            start_ranges[start_tuples[0][2]] = {1}
            for v in start_ranges:
                if v == start_tuples[0][2]:
                    continue
                start_ranges[v] -= {1}
        return extend(start_tuples, start_ranges, 0)


puzzle = Puzzle(open(sys.argv[1], "r"))
puzzle.show()
print()
vals = puzzle.solve()
if vals is None:
    print("unsat")
else:
    puzzle.show(vals)

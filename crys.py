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

        # Read the three instance lines.
        lines = [read_line() for _ in range(3)]

        # Normalize the line lengths by padding with "letter" 0.
        max_width = max([len(l) for l in lines])
        self.lines = [ ["0"] * (max_width - len(l)) + l for l in lines ]

        # Order the variables right-to-left top-to-bottom.
        vars = []
        for i in range(3):
            for c in self.lines[i]:
                if c == "0" or c in vars:
                    continue
                vars.append(c)

        self.vars = vars
        self.vals = dict()
    
    def show(self):
        max_width = max([len(l) for l in self.lines])
        for l in self.lines:
            width = len(l)
            for _ in range(max_width - width):
                print(" ", end="")
            for c in l:
                if c == "0":
                    print(" ", end="")
                elif c in self.vals:
                    print(self.vals[c], end="")
                else:
                    print(c, end="")
            print()

    def solve(self):

        # Return 1 if puzzle is solved,
        # 0 if puzzle is partially solved,
        # -1 if state is illegal.
        def check():

            def value(var):
                if var == "0":
                    return 0;
                if var in self.vals:
                    return self.vals[var]
                return None

            carry = 0
            for d1 in reversed(self.lines[0]):
                v1 = value(d1)
                if v1 is None:
                    return 0
                for d2 in reversed(self.lines[1]):
                    v2 = value(d2)
                    if v2 is None:
                        return 0
                    for s in reversed(self.lines[2]):
                        vs = value(s)
                        if vs is None:
                            return 0
                        total = v1 + v2 + carry
                        if total % 10 != vs:
                            return -1
                        carry = total - total % 10

            if carry != 0:
                return -1
            
        unused = sorted(set(range(10)) - set(self.vals.values()))
        for v in self.vars:
            if v in self.vals:
                continue
            for val in unused:
                self.vals[v] = val
                status = check()
                if status == 1:
                    return True
                if status == -1:
                    del self.vals[v]
                    continue
                result = self.solve()
                if result:
                    return True
                del self.vals[v]

        if not self.vals:
            return None
        return self.vals

puzzle = Puzzle(open(sys.argv[1], "r"))
puzzle.show()
print(puzzle.solve())
puzzle.show()

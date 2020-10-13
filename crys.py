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
        # XXX vars is a Python built-in, so pvars.
        pvars = []
        for i in range(3):
            for c in self.lines[i]:
                if c == "0" or c in pvars:
                    continue
                pvars.append(c)
        self.pvars = pvars

        # List of tuples forming the equation.
        tuples = []
        for d1 in self.lines[0]:
            for d2 in self.lines[1]:
                for s in self.lines[2]:
                    tuples.append((d1, d2, s))
        self.tuples = reversed(tuples)
    
    def show(self, vals=dict()):
        max_width = max([len(l) for l in self.lines])
        for l in self.lines:
            width = len(l)
            for _ in range(max_width - width):
                print(" ", end="")
            for c in l:
                if c == "0":
                    print(" ", end="")
                elif c in vals:
                    print(vals[c], end="")
                else:
                    print(c, end="")
            print()

    def solve(self, pvars=None, vals=None):
        # New solution attempt. Can't put these values
        # inline because bad things happen with Python's
        # evaluator.
        if pvars is None:
            pvars = list(self.pvars)
        if vals is None:
            vals = dict()

        # Return the value of the variable,
        # or None if unvalued.
        def value(var):
            if var == "0":
                return 0;
            if var in vals:
                return vals[var]
            return None

        # Return True iff no constraint violations
        def ok():
            carry = 0
            for d1, d2, s in self.tuples:
                if carry is None:
                    continue
                v1, v2, vs = map(value, (d1, d2, s))
                if None in (v1, v2):
                    carry = None
                    continue
                total = v1 + v2 + carry
                if vs is not None and total % 10 != vs:
                    return False
                carry = total - total % 10

            if carry == 1:
                return False
            return True

        # Base case: check for solution.
        if not pvars:
            return vals

        # Base case: check for failure.
        if not ok():
            return None

        # Recursive case: try to extend partial assignment.
        unused = sorted(list(set(range(10)) - set(vals.values())))
        v = pvars.pop()
        assert v not in vals
        for val in unused:
            vals[v] = val
            soln = self.solve(pvars=pvars, vals=vals)
            if soln:
                return soln

        del vals[v]
        pvars.append(v)
        return None

puzzle = Puzzle(open(sys.argv[1], "r"))
puzzle.show()
vals = puzzle.solve()
print(vals)
puzzle.show(vals)

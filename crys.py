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
        for j in reversed(range(max_width)):
            for i in range(3):
                c = self.lines[i][j]
                if c == "0" or c in pvars:
                    continue
                pvars.append(c)
        self.pvars = pvars

        # List of tuples forming the equation.
        l = self.lines
        tuples = [(l[0][i], l[1][i], l[2][i]) for i in range(max_width)]
        self.tuples = list(reversed(tuples))
    
    def show(self, vals=dict()):
        for l in self.lines:
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

        # Return True iff no constraint violations
        def ok():
            # Return the value of the variable,
            # or None if unvalued.
            def value(var):
                if var == "0":
                    return 0;
                if var in vals:
                    return vals[var]
                return None

            carry = 0
            for d1, d2, s in self.tuples:
                v1, v2, vs = map(value, (d1, d2, s))
                if None in (v1, v2):
                    return True
                total = v1 + v2 + carry
                if vs is not None and total % 10 != vs:
                    return False
                carry = total // 10
                assert carry in {0, 1}

            return carry == 0

        print("solve", pvars, vals)

        # Base case: check for failure.
        if not ok():
            print("fail")
            return None

        # Base case: check for solution.
        if not pvars:
            print("succeed")
            return vals

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
if vals is not None:
    puzzle.show(vals)

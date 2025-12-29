#! env python

"""
BinOXXO Program Solver

Uses the Z3 Theorem Prover.
"""

import argparse
from tools import Grider
from z3 import Int, Solver, sat, And, Sum, Distinct


class BinOXXO:

    def __init__(self, filename: str):
        self.grider = Grider(filename)
        self.grid = self.grider.grid
        print("initial grid")
        self.grider.print_grid(self.grid)

    def solve(self) -> None:
        # Get the grid size from the input.
        n = len(self.grid)

        solver = Solver()

        # Int variables for grid cells: 0 for 'o', 1 for 'x'.
        x = [[Int(f"x_{r}_{c}") for c in range(n)] for r in range(n)]

        # Bound constraints.
        for r in range(n):
            for c in range(n):
                solver.add(And(x[r][c] >= 0, x[r][c] <= 1))

        # Set constraints for preset cells.
        for r in range(n):
            for c in range(n):
                if self.grid[r][c] == "x":
                    solver.add(x[r][c] == 1)
                elif self.grid[r][c] == "o":
                    solver.add(x[r][c] == 0)

        # No three consecutive cells are identical (row and column).
        for i in range(n):
            for j in range(n - 2):
                # in rows
                solver.add(
                    x[i][j] + x[i][j + 1] + x[i][j + 2] >= 1
                )  # At least one x in three
                solver.add(
                    x[i][j] + x[i][j + 1] + x[i][j + 2] <= 2
                )  # At most two x in three
                # in columns
                solver.add(x[j][i] + x[j + 1][i] + x[j + 2][i] >= 1)
                solver.add(x[j][i] + x[j + 1][i] + x[j + 2][i] <= 2)

        # Same number of o and x per row/column.
        target_count = n // 2
        for i in range(n):
            solver.add(sum(x[i][j] for j in range(n)) == target_count)
            solver.add(sum(x[j][i] for j in range(n)) == target_count)

        # No two rows or columns can be identical.
        # As a binary number a row or column can represent a number
        # between 0 and 2**n - 1. These numbers should all be
        # different per row or column.
        def add_uniqueness_constraints(solver, vectors, prefix):
            fingerprints = []
            for r, vec in enumerate(vectors):
                # 1. Create a Z3 integer variable.
                # Z3 Ints are mathematical (unbounded), so we add range constraints.
                fp = Int(f"fp_{prefix}_{r}")
                solver.add(fp >= 0, fp < 2**n)

                # 2. Map the vector to a single integer value (fingerprint)
                # Sum() in Z3 takes a list of expressions
                solver.add(Sum([vec[i] * (2**i) for i in range(n)]) == fp)
                fingerprints.append(fp)

            # 3. Ensure all fingerprints are unique
            solver.add(Distinct(fingerprints))

        add_uniqueness_constraints(solver, x, "r")  # rows
        add_uniqueness_constraints(
            solver, [[x[r][c] for r in range(n)] for c in range(n)], "c"
        )  # columns

        # Get solver and solve the model.
        if solver.check() == sat:
            model = solver.model()
            stats = solver.statistics()

            print(f"solved in {stats.time:.3f} s with")
            sol = []
            for r in range(n):
                sol.append(["x" if model.eval(x[r][c]) == 1 else "o" for c in range(n)])
            self.grider.print_grid(sol)
        else:
            print(f"problem!")


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="produce more verbose output"
    )
    parser.add_argument("-f", "--file", type=str, help="input file")

    args = parser.parse_args()

    print(f"BinOXXO using Z3\n")

    if args.file:
        binoxxo = BinOXXO(args.file)
        binoxxo.solve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

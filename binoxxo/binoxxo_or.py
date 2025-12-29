#! env python

"""
BinOXXO Program Solver

Uses the OR-Tools CP-SAT solver.
"""

import argparse
from tools import Grider
from ortools.sat.python import cp_model


class BinOXXO:

    def __init__(self, filename: str):
        self.grider = Grider(filename)
        self.grid = self.grider.grid
        print("initial grid")
        self.grider.print_grid(self.grid)

    def solve(self) -> None:
        # Get the grid size from the input.
        n = len(self.grid)

        model = cp_model.CpModel()

        # Variables for cells: 0 for 'o', 1 for 'x'.
        x = [[model.NewIntVar(0, 1, f"x_{r}_{c}") for c in range(n)] for r in range(n)]

        # Set constraints for preset cells.
        for r in range(n):
            for c in range(n):
                if self.grid[r][c] == "x":
                    model.Add(x[r][c] == 1)
                elif self.grid[r][c] == "o":
                    model.Add(x[r][c] == 0)

        # No three consecutive cells are identical (row and column).
        for i in range(n):
            for j in range(n - 2):
                # in rows
                model.Add(
                    x[i][j] + x[i][j + 1] + x[i][j + 2] >= 1
                )  # At least one x in three
                model.Add(
                    x[i][j] + x[i][j + 1] + x[i][j + 2] <= 2
                )  # At most two x in three
                # in columns
                model.Add(x[j][i] + x[j + 1][i] + x[j + 2][i] >= 1)
                model.Add(x[j][i] + x[j + 1][i] + x[j + 2][i] <= 2)

        # Same number of o and x per row/column.
        target_count = n // 2
        for i in range(n):
            model.Add(sum(x[i][j] for j in range(n)) == target_count)
            model.Add(sum(x[j][i] for j in range(n)) == target_count)

        # No two rows or columns can be identical.
        # As a binary number a row or column can represent a number
        # between 0 and 2**n - 1. These numbers should all be
        # different per row or column.
        def add_uniqueness_constraints(model, vectors):
            fingerprints = []
            for vec in vectors:
                fp = model.NewIntVar(0, 2**n - 1, "")
                model.Add(sum(vec[i] * (2**i) for i in range(n)) == fp)
                fingerprints.append(fp)
            model.AddAllDifferent(fingerprints)

        add_uniqueness_constraints(model, x)  # rows
        add_uniqueness_constraints(
            model, [[x[r][c] for r in range(n)] for c in range(n)]
        )  # columns

        # Get solver and solve the model.
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        # https://developers.google.com/optimization/cp/cp_solver#cp-sat_return_values

        if status == cp_model.OPTIMAL:
            msg = "OPT"
        elif status == cp_model.FEASIBLE:
            msg = "FEASIBLE"
        elif status == cp_model.INFEASIBLE:
            msg = "INFEASIBLE"
        elif status == cp_model.MODEL_INVALID:
            msg = "MODEL_INVALID"
        else:
            msg = "UNKNOWN"

        if status == cp_model.OPTIMAL or cp_model.FEASIBLE:
            print(f"solved in {solver.WallTime():.3f} s with {msg}")
            sol = []
            for r in range(n):
                sol.append(
                    ["x" if solver.Value(x[r][c]) == 1 else "o" for c in range(n)]
                )
            self.grider.print_grid(sol)
        else:
            print(f"problem: {msg}")


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="produce more verbose output"
    )
    parser.add_argument("-f", "--file", type=str, help="input file")

    args = parser.parse_args()

    print(f"BinOXXO using CP-SAT\n")

    if args.file:
        binoxxo = BinOXXO(args.file)
        binoxxo.solve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

"""
BinOXXO Program Solver

Rules for prefilling.
"""

import numpy as np


SIDE = 10


def patterns_main(grid: np.ndarray) -> int:
    """Do simple patterns across all rows.
    Return the number of changed items."""

    empty_two_o = ["", "o", "o"]
    two_o_empty = ["o", "o", ""]

    empty_two_x = ["", "x", "x"]
    two_x_empty = ["x", "x", ""]

    o_empty_o = ["o", "", "o"]
    x_empty_x = ["x", "", "x"]

    nb_changed = 0
    for i in range(SIDE):
        for j in range(SIDE - 2):
            if (grid[i, j : j + 3] == empty_two_o).all():
                grid[i, j] = "x"
                nb_changed += 1
            if (grid[i, j : j + 3] == two_o_empty).all():
                grid[i, j + 2] = "x"
                nb_changed += 1
            if (grid[i, j : j + 3] == empty_two_x).all():
                grid[i, j] = "o"
                nb_changed += 1
            if (grid[i, j : j + 3] == two_x_empty).all():
                grid[i, j + 2] = "o"
                nb_changed += 1
            if (grid[i, j : j + 3] == o_empty_o).all():
                grid[i, j + 1] = "x"
                nb_changed += 1
            if (grid[i, j : j + 3] == x_empty_x).all():
                grid[i, j + 1] = "o"
                nb_changed += 1
    return nb_changed


def patterns(grid: np.ndarray) -> int:
    """Fill simple patterns across all columns by transposing the grid.
    Return the number of changed items."""
    nb_changed = patterns_main(grid)

    grid = grid.T
    nb_changed = patterns_main(grid)
    grid = grid.T
    return nb_changed


def fill_single(gridline: np.ndarray, e: str) -> int | None:
    """Fill a single gridline (line or colum)."""

    if gridline[0] == "" and gridline[1] != "":
        gridline[0] = e
        return 1

    if gridline[SIDE - 1] == "" and gridline[SIDE - 2] != "":
        gridline[SIDE - 1] = e
        return 1

    for i in range(1, SIDE - 1):
        # print("> ", gridline[i-1], gridline[i], gridline[i+1])
        if gridline[i - 1] != "" and gridline[i] == "" and gridline[i + 1] != "":
            gridline[i] = e
            return 1

    print("should never happen")
    print(gridline)


def count(gridline: np.ndarray) -> tuple[int]:
    """Count the number of symbols and empty spots."""

    x = np.isin(gridline, "x").sum()
    o = np.isin(gridline, "o").sum()
    return x, o, SIDE - x - o


def singles_main(grid: np.ndarray) -> int:
    nb_changed = 0

    for i in range(SIDE):
        x, o, empty = count(grid[i, :])
        if o == 5 and empty > 0:
            grid[i, grid[i, :] == ""] = "x"
            nb_changed += 1
        elif x == 5 and empty > 0:
            grid[i, grid[i, :] == ""] = "o"
            nb_changed += 1

    return nb_changed


def singles(grid: np.ndarray) -> int:
    nb_changed = singles_main(grid)

    grid = grid.T
    nb_changed += singles_main(grid)
    grid = grid.T

    return nb_changed


def triplets_main(grid: np.ndarray) -> int:

    p1 = ["x", "", ""]
    p2 = ["", "", "x"]
    p3 = ["", "", "o"]
    p4 = ["o", "", ""]
    triple_space = ["", "", ""]

    nb_changed = 0

    for i in range(SIDE):

        not_triple_space = True
        for j in range(SIDE - 2):
            if (grid[i, j : j + 3] == triple_space).all():
                not_triple_space = False

        if not_triple_space:
            x, o, empty = count(grid[i, :])
            if x == 3 and o == 4:
                for j in range(SIDE - 2):
                    if (grid[i, j : j + 3] == p1).all() or (
                        grid[i, j : j + 3] == p2
                    ).all():
                        nb_changed += fill_single(grid[i, :], "x")
                        break
            elif x == 4 and o == 3:
                for j in range(SIDE - 2):
                    if (grid[i, j : j + 3] == p3).all() or (
                        grid[i, j : j + 3] == p4
                    ).all():
                        nb_changed += fill_single(grid[i, :], "o")
                        break
    return nb_changed


def triplets(grid: np.ndarray) -> int:
    nb_changed = triplets_main(grid)

    grid = grid.T
    nb_changed += triplets_main(grid)
    grid = grid.T

    return nb_changed


def quintuplets_main(grid: np.ndarray) -> int:

    p1 = ["x", "", "", "", "x"]
    p2 = ["o", "", "", "", "o"]
    p3 = ["o", "", "", "", "x"]
    p4 = ["x", "", "", "", "o"]

    nb_changed = 0

    for i in range(SIDE):
        x, o, empty = count(grid[i, :])
        if x == 3 and o == 4:
            for j in range(SIDE - 4):
                if (grid[i, j : j + 5] == p1).all():
                    grid[i, j + 2] = "o"  # ['x','','o','','x']
                    nb_changed += 1
                    break
                if (grid[i, j : j + 5] == p3).all():
                    grid[i, j + 1] = "x"  # ['o','x','','','x']
                    nb_changed += 1
                    break
                if (grid[i, j : j + 5] == p4).all():
                    grid[i, j + 3] = "x"  # ['x','','','x','o']
                    nb_changed += 1
                    break
        elif o == 3 and x == 4:
            for j in range(SIDE - 4):
                if (grid[i, j : j + 5] == p2).all():
                    grid[i, j + 2] = "x"  # ['o','','x','','o']
                    nb_changed += 1
                    break
                if (grid[i, j : j + 5] == p3).all():
                    grid[i, j + 3] = "o"  # ['o','','','o','x']
                    nb_changed += 1
                    break
                if (grid[i, j : j + 5] == p4).all():
                    grid[i, j + 1] = "o"  # ['x','o','','','o']
                    nb_changed += 1
                    break
    return nb_changed


def quintuplets(grid: np.ndarray) -> int:
    nb_changed = quintuplets_main(grid)

    grid = grid.T
    nb_changed += quintuplets_main(grid)
    grid = grid.T

    return nb_changed


def heuristics(grid: np.ndarray) -> None:
    """Main entry point to heuristics."""

    while True:
        s = patterns(grid)
        s += singles(grid)
        s += triplets(grid)
        s += quintuplets(grid)

        # if no rule has changed something, abort!
        if s == 0:
            break

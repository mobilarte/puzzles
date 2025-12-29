#! env python

"""
BinOXXO Program Solver

Uses rules and brute-force approach.
"""

import argparse
from tools import Grider
from heuristics import heuristics, SIDE


import numpy as np

verbose_on = False


def grid_is_valid(grid: np.ndarray) -> bool:
    """Check for valid grid."""

    # cannot have more 5 symbols per row/column
    for i in [0, 1]:
        xs = (np.count_nonzero(grid == "x", axis=i) > 5).any()
        os = (np.count_nonzero(grid == "o", axis=i) > 5).any()
        if xs or os:
            return False

    # cannot have more than 3 consecutive symbols per row/column
    os = ["o", "o", "o"]
    xs = ["x", "x", "x"]
    for i in range(SIDE):
        for j in range(SIDE - 2):
            if (grid[i, j : j + 3] == xs).all() or (grid[i, j : j + 3] == os).all():
                return False
    for j in range(SIDE):
        for i in range(SIDE - 2):
            if (grid[i : i + 3, j] == xs).all() or (grid[i : i + 3, j] == os).all():
                return False

    # cannot have two identical rows/columns, but only when they are full!
    for i in range(SIDE - 1):
        for j in range(i + 1, SIDE):
            if (
                grid_full(grid[i, :])
                and grid_full(grid[j, :])
                and (grid[i, :] == grid[j, :]).all()
            ):
                # print(f"identical rows {i},{j}")
                return False
    for i in range(SIDE - 1):
        for j in range(i + 1, SIDE):
            if (
                grid_full(grid[:, i])
                and grid_full(grid[:, j])
                and (grid[:, i] == grid[:, j]).all()
            ):
                # print(f"identical columns {i},{j}")
                return False
    return True


def grid_full(grid: np.ndarray) -> bool:
    """Return True if the (partial) grid is full."""
    return np.count_nonzero(grid == "") == 0


def empty_index(grid: np.ndarray) -> list[list[int, int]]:
    return np.argwhere(grid == "")


def solve_grid(grid: np.ndarray, empty_list: np.ndarray) -> bool:
    """Entry point to the recursive solver."""

    if grid_full(grid):  # empty_list.shape[0] == 0:
        if grid_is_valid(grid):
            return True
        else:
            return False

    i, j = empty_list[0]
    for v in ["o", "x"]:
        # set tentative position
        grid[i, j] = v
        if grid_is_valid(grid) and solve_grid(grid, empty_list[1:]):
            return True
        # reset position
        grid[i, j] = ""
    return False


def play_game(filename: str, prefill: bool) -> None:
    """Initialize the game and play it."""

    grider = Grider(filename)
    grid = grider.as_np()

    if not grid_is_valid(grid):
        print("invalid grid")
        return

    print("initial grid")
    grider.print_grid(grid)

    if prefill:
        print("starting prefilling")
        heuristics(grid)
        grider.print_np_grid(grid)

    if grid_full(grid):
        print("solution found with prefilling or already full")
        grider.print_np_grid(grid)
    else:
        print("starting exhaustive search")
        if grid_is_valid(grid) and solve_grid(grid, empty_index(grid)):
            grider.print_grid(grid)
        else:
            print("cannot find a solution, sorry!")


def main() -> None:

    global verbose_on

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="produce more verbose output"
    )
    parser.add_argument("-f", "--file", type=str, help="input file")
    parser.add_argument(
        "-p", "--prefill", action="store_true", help="use heuristics to prefill"
    )

    args = parser.parse_args()

    verbose_on = args.verbose

    print("binoxxo is the name of the game")
    play_game(args.file, args.prefill)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

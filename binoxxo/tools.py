import numpy as np


class Grider:

    def __init__(self, filename: str):
        """Read a text, ignoring comments and empty lines,
        return as a list of list of strings."""

        try:
            with open(filename) as f:
                s = f.readlines()

            s = [
                line.strip()
                for line in s
                if not line.startswith("#")
                and not len(line) == 0
                and not line.isspace()
            ]

            s = "".join(s).replace("-", " ").lower()
            n = int(np.sqrt(len(s)))
            self.grid = [[s[i] for i in range(j * n, j * n + n)] for j in range(n)]
        except Exception as err:
            print(err)
            exit(1)

    def as_np(self) -> np.array:
        g =  np.array(self.grid)
        g[g == " "] = ""
        return g

    def print_grid(self, grid: list[list[str]]) -> None:
        """Print a grid nicely."""

        n = len(grid)
        print("")
        for r in range(n):
            for c in range(n):
                if grid[r][c] == "" or grid[r][c] == " ":
                    print(" . ", end="")
                else:
                    print(f" {grid[r][c]} ", end="")
            print("")
        print("")
        
    def print_np_grid(self, grid: np.array) -> None:
        self.print_grid(grid.tolist())

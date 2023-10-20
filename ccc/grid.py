from typing import List, Set, Tuple

WATER_MARK = "W"

class Grid:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid  # use grid[y][x] to access
        self.size = len(grid)
        self.islands: List[Set[Tuple[int, int]]] = []

        # print(self._discover_island(4, 2))

    def discover_island(self, x: int, y: int):
        island = {(x, y)}
        to_observe = {(x, y)}

        while to_observe:
            x, y = to_observe.pop()
            for xn, yn in self._neighbours(x, y):
                if (xn, yn) in island:
                    continue
                island.add((xn, yn))
                to_observe.add((xn, yn))

        return island

    def _neighbours(self, x: int, y: int):
        candidates = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        for xc, yc in candidates:
            if xc < 0 or xc >= self.size:
                continue  # out of bounds
            if yc < 0 or yc >= self.size:
                continue  # out of bounds
            if self.grid[yc][xc] == WATER_MARK:
                continue  # in water
            yield xc, yc
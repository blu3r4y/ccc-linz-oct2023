from typing import List, Set, Tuple

from pathfinding import astar_search, manhattan_distance, reconstruct_path
from routes import check_intersect

WATER_MARK = "W"
LAND_MARK = "L"


class Grid:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid  # use grid[y][x] to access
        self.size = len(grid)
        self.islands: List[Set[Tuple[int, int]]] = []

        # print(self._discover_island(4, 2))

    def find_route(self, a: Tuple[int, int], b: Tuple[int, int]):
        print(f"find_route({a}, {b})")

        def __get_successors(xy: Tuple[int, int]):
            yield from self._neighbours_water(xy[0], xy[1])

        route = astar_search(a, b, __get_successors, manhattan_distance)
        assert not check_intersect(route)
        return route

    def discover_island(self, x: int, y: int):
        island = {(x, y)}
        to_observe = {(x, y)}

        while to_observe:
            x, y = to_observe.pop()
            for xn, yn in self._neighbours_land(x, y):
                if (xn, yn) in island:
                    continue
                island.add((xn, yn))
                to_observe.add((xn, yn))

        return island

    def _neighbours_water(self, x: int, y: int):
        yield from self.__neighbours(x, y, LAND_MARK, diagonal=True)

    def _neighbours_land(self, x: int, y: int):
        yield from self.__neighbours(x, y, WATER_MARK)

    def __neighbours(self, x: int, y: int, avoid: str, diagonal: bool = False):
        candidates = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        if diagonal:
            candidates += [
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y + 1),
            ]

        for xc, yc in candidates:
            if xc < 0 or xc >= self.size:
                continue  # out of bounds
            if yc < 0 or yc >= self.size:
                continue  # out of bounds
            if self.grid[yc][xc] == avoid:
                continue
            yield xc, yc

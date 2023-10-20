from typing import List, Set, Tuple

from pathfinding import astar_search, manhattan_distance, reconstruct_path
from routes import check_intersect
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d

WATER_MARK = "W"
LAND_MARK = "L"


class Grid:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid  # use grid[y][x] to access
        self.size = len(grid)
        self.islands: List[Set[Tuple[int, int]]] = []

        # print(self._discover_island(4, 2))

    def bring_route_in_order(self, route: List[Tuple[int, int]]):
        # compute convex hull
        assert len(route) > 0
        points = np.array(list(route))
        hull = ConvexHull(points)

        # plt.plot(points[:,0], points[:,1], 'o')
        # for simplex in hull.simplices:
        #     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
        # plt.show()

        vertices = set()
        for vi in hull.vertices:
            vertices.add((int(points[vi, 0]), int(points[vi, 1])))
        vertices = list(vertices)
        print(vertices)

        # find the two points that have the longest distance to each other
        max_distance = 0
        max_a, max_b = None, None
        for a, b in zip(vertices, vertices[1:]):
            distance = self.distance(a, b)
            if distance > max_distance:
                max_distance = distance
                max_a, max_b = a, b

        unconnected = vertices[1:]
        connected = [vertices[0]]

        def __get_successors(xy: Tuple[int, int]):
            yield from self._neighbours_for_ships(xy[0], xy[1])

        while unconnected:
            last_point = connected[-1]
            # sort by euclidean distance to next point
            # candidates = sorted(unconnected, key=lambda c: self.distance(c, last_point))
            candidate = unconnected[0]

            route = astar_search(last_point, candidate, __get_successors, manhattan_distance)
            assert route is not None, f"no route from {last_point} to {candidate}"
            for point in route[1:]:
                connected.append(point)
                if point in unconnected:
                    unconnected.remove(point)

        # connect back to the first point
        first_neighbours = set(self._neighbours_for_ships(connected[0][0], connected[0][1]))
        if connected[-1] not in first_neighbours:
            route = astar_search(connected[-1], connected[0], __get_successors, manhattan_distance)
            assert route is not None, f"no route back to start"
            for point in route[1:-1]:
                connected.append(point)

        print("connected", connected)

        plt.plot(points[:,0], points[:,1], 'o')
        plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=0.5)
        plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
        for a, b in zip(connected, connected[1:]):
            plt.plot([a[0], b[0]], [a[1], b[1]], 'b', lw=3, alpha=0.3)
        plt.show()

        # ensure that the route is continuous
        self.ensure_continuous_path(connected)

        # ensure that the route ends at a neighbour of the first point
        first_neighbours = set(self._neighbours_for_ships(connected[0][0], connected[0][1]))
        assert connected[-1] in first_neighbours, f"last point {connected[-1]} is not a neighbour of {connected[0]}"

        return connected

    def get_island_fringe(self, x: int, y: int):
        # (x,y) is any point on that island
        island = self.discover_island(x, y)
        outer = island.copy()

        for x, y in island:
            outer.update(self._neighbours_for_island_fringe(x, y))

        # subtract island from outer
        fringe = outer - island
        return fringe

    def ensure_continuous_path(self, route: List[Tuple[int, int]]):
        for a, b in zip(route, route[1:]):
            euclidean_distance = self.distance(a, b)
            assert euclidean_distance < 2, f"distance between {a} <-> {b} is {euclidean_distance}"

    def distance(self, a: Tuple[int, int], b: Tuple[int, int]):
        # euclidean distance
        x1, y1 = a
        x2, y2 = b
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def find_route(self, a: Tuple[int, int], b: Tuple[int, int]):

        def __get_successors(xy: Tuple[int, int]):
            yield from self._neighbours_for_ships(xy[0], xy[1])

        route = astar_search(a, b, __get_successors, manhattan_distance)
        assert not check_intersect(route)
        return route

    def discover_island(self, x: int, y: int):
        island = {(x, y)}
        to_observe = {(x, y)}

        while to_observe:
            x, y = to_observe.pop()
            for xn, yn in self._neighbours_for_land(x, y):
                if (xn, yn) in island:
                    continue
                island.add((xn, yn))
                to_observe.add((xn, yn))

        return island

    def _neighbours_for_ships(self, x: int, y: int):
        yield from self.__neighbours(x, y, avoid=LAND_MARK, diagonal=True)

    def _neighbours_for_island_fringe(self, x: int, y: int):
        yield from self.__neighbours(x, y, avoid=LAND_MARK, diagonal=False)

    def _neighbours_for_land(self, x: int, y: int):
        yield from self.__neighbours(x, y, avoid=WATER_MARK, diagonal=False)

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

    # def bring_route_in_order(self, route: List[Tuple[int, int]]):
    #     route = set(route)
    #     g = nx.Graph()
    #     for x, y in route:
    #         possible_edges = set(self._neighbours_for_ships(x, y))
    #         possible_edges = possible_edges.intersection(route)
    #         for xn, yn in possible_edges:
    #             g.add_edge((x, y), (xn, yn))
    #
    #     # compute convex hull
    #     points = np.array(list(g.nodes))
    #     hull = ConvexHull(points, incremental=True)
    #     print(hull.simplices)
    #
    #     plt.plot(points[:,0], points[:,1], 'o')
    #     for simplex in hull.simplices:
    #         plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
    #     plt.show()
    #
    #     # get simple cycles
    #     simple_cycles = list(nx.simple_cycles(g))
    #
    #     # return largest cycle
    #     simple_cycles = sorted(simple_cycles, key=lambda c: len(c), reverse=True)
    #     return simple_cycles[0]

    # def bring_route_in_order(self, route: List[Tuple[int, int]]):
    #     assert len(route) > 0
    #     route = sorted(route)
    #     open_list = set(route[1:])
    #     ordered_route = [route[0]]
    #
    #     while open_list:
    #         xl, yl = ordered_route[-1]
    #         candidates = set(self._neighbours_for_ships(xl, yl))
    #         candidates = candidates.intersection(open_list)
    #
    #         assert len(candidates) > 0, f"no candidates for {xl},{yl}"
    #
    #         # take the one that is FURTHER away
    #         candidates = sorted(candidates, key=lambda c: self.distance(c, (xl, yl)))
    #         selected = candidates[-1]
    #
    #         ordered_route.append(selected)
    #         open_list.remove(selected)
    #
    #     # ensure that the route ends at a neighbour of the first point
    #     first_neighbours = set(self._neighbours_for_ships(ordered_route[0][0], ordered_route[0][1]))
    #     if ordered_route[-1] not in first_neighbours:
    #         print("debug")
    #     assert ordered_route[-1] in first_neighbours, f"last point {ordered_route[-1]} is not a neighbour of {ordered_route[0]}"
    #
    #     self.ensure_continuous_path(ordered_route)
    #
    #     return ordered_route
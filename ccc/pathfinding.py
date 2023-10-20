from queue import PriorityQueue
from typing import Tuple


def astar_search(start: Tuple[int, int], goal: Tuple[int, int], get_successors, estimate_distance):
    openpq = PriorityQueue()
    openpq.put((0, 0, start))
    closed = {start: 0}
    parents = {start: None}
    tiebreaker = 1

    while not openpq.empty():
        _, _, current = openpq.get()
        if current == goal:
            return reconstruct_path(parents, start, goal)

        for succ in get_successors(current):
            new_cost = closed[current] + 1
            if succ not in closed:
                parents[succ] = current
                closed[succ] = new_cost
                estimate = new_cost + estimate_distance(succ, goal)
                openpq.put((estimate, tiebreaker, succ))
                tiebreaker += 1

    return None


def reconstruct_path(parents, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    return path

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

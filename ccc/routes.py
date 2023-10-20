from typing import List, Tuple


def check_intersect(route: List[Tuple[int, int]]):
    length = len(route)
    if length != len(set(route)):
        return True  # duplicate points

    forbidden = set()

    # iterate over (x,y) pairs with window size 2
    for (x1, y1), (x2, y2) in zip(route, route[1:]):
        if ((x1, y1), (x2, y2)) in forbidden:
            return True

        vec_type = _identify_vector_type((x1, y1), (x2, y2))
        if vec_type == "d+" or vec_type == "d-":
            # block the other two diagonals
            forbidden.add(((x1, y2), (x2, y1)))
            forbidden.add(((x2, y1), (x1, y2)))

    return False


def _identify_vector_type(a: Tuple[int, int], b: Tuple[int, int]) -> str:
    # check if a -> b is horizontal, vertical,
    # or diagonal (positive, negative)
    ax, ay = a
    bx, by = b

    if ax == bx:
        return "v"
    if ay == by:
        return "h"
    if ax < bx:
        if ay < by:
            return "d+"
        else:
            return "d-"
    else:
        if ay < by:
            return "d-"
        else:
            return "d+"

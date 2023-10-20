from grid import Grid
from routes import check_intersect


def solve(data):
    g = Grid(data["grid"])

    result = []
    for coord in data["coords"]:
        fringe = g.get_island_fringe(coord[0][0], coord[0][1])
        route = g.bring_route_in_order(fringe)
        assert not check_intersect(route)
        route_str = " ".join(map(lambda xy: f"{xy[0]},{xy[1]}", route))
        result.append(route_str)

    return "\n".join(result)

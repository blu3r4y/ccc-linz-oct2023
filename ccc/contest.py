from grid import Grid
from routes import check_intersect


def solve(data):
    g = Grid(data["grid"])

    result = []
    for a, b in data["coords"]:
        route = g.find_route(a, b)
        route_str = " ".join(map(lambda xy: f"{xy[0]},{xy[1]}", route))
        result.append(route_str)

    return "\n".join(result)

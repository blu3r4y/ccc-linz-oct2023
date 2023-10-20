from grid import Grid
from routes import check_intersect


def solve(data):

    # g = Grid(data["grid"])

    result = []
    for route in data["coords"]:
        if check_intersect(route):
            result.append("INVALID")
        else:
            result.append("VALID")

    return "\n".join(result)

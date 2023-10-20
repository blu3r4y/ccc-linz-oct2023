from grid import Grid

def solve(data):

    g = Grid(data["grid"])

    result = []
    for (x1, y1), (x2, y2) in data["coords"]:
        i = g.discover_island(x1, y1)
        if (x2, y2) in i:
            result.append("SAME")
        else:
            result.append("DIFFERENT")

    return "\n".join(result)

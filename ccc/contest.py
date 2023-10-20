def solve(data):
    coords = data["coords"]
    grid = data["grid"]

    result = []
    for coord in coords:
        x, y = coord
        result.append(grid[y][x])

    return "\n".join(result)

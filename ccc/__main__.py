from pprint import pprint
from pathlib import Path

from loguru import logger as log

from .utils import infer_current_level, infer_quests_for_level
from .contest import solve


def load(data):
    size_of_map = int(data[0])
    grid = data[1:size_of_map + 1]
    num_coords = int(data[size_of_map + 1])
    coords_str = data[size_of_map + 2 : size_of_map + 2 + num_coords]
    coords = [tuple(map(int, c.split(","))) for c in coords_str]
    return {"size": size_of_map, "grid": grid, "n_coords": num_coords, "coords": coords}


if __name__ == "__main__":
    base_path = Path("../data")
    level = infer_current_level(base_path)
    quests = infer_quests_for_level(base_path, level)


    for quest in quests:
        input_file = base_path / f"level{level}_{quest}.in"
        output_file = input_file.with_suffix(".out")

        if not input_file.exists():
            log.warning(f"file not found, skip: {input_file}")
            continue

        with open(input_file, "r") as fi:
            data = load(fi.read().splitlines())
            pprint(data)

            print("=== Input {}".format(quest))
            print("======================")

            result = solve(data)
            pprint(result)

            with open(output_file, "w+") as fo:
                fo.write(result)

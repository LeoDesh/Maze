import os
import random
from typing import Tuple, List, Dict


def transform_single_coordinates(tup: Tuple[int], width):
    x, y = tup
    return (y, width - x + 1)


def transform_coordinates(
    path: List[Tuple[int, int]], width: int
) -> List[Tuple[int, int]]:
    return [transform_single_coordinates(tup, width) for tup in path]


def retransform_coordinates(
    path: List[Tuple[int, int]], width: int
) -> List[Tuple[int, int]]:
    return [(-(y - width - 1), x) for (x, y) in path]


def process_path(path: str, relative_backwards: str):
    folders = path.split("\\")
    count = relative_backwards.count(".")
    return "\\".join(folders[i] for i in range(len(folders) - count))


def add_tuples(t1: tuple, t2: tuple):
    return tuple(s + t for s, t in zip(t1, t2))


def verify_file(path: str):
    if not os.path.isfile(path):
        raise ValueError(f"Provided path {path} does not lead to a file!")
    if not path.split(".")[-1] == "txt":
        raise TypeError(
            f"Provided file must be a txt file, not a {path.split('.')[-1]} file!"
        )


def verify_ending(path: str):
    if not path.split(".")[-1] == "txt":
        raise TypeError(
            f"Provided file must be a txt file, not a {path.split('.')[-1]} file!"
        )


def subtract_tuples(t1: tuple, t2: tuple):
    return tuple(s - t for s, t in zip(t1, t2))


def find_value_in_config(value: int, maze_config: List[List[int]]):
    width = len(maze_config)
    length = len(maze_config[0])
    for i in range(width):
        for j in range(length):
            if value == maze_config[i][j]:
                return True
    return False


def construct_bfs_path(key_index: str, dict_path: Dict[str, List[Tuple[int, int]]]):
    delimiter = "."
    if delimiter in key_index:
        numbers = key_index.split(delimiter)
        key_indices = [
            ".".join(number for number in numbers[: i + 1])
            for i, _ in enumerate(numbers)
        ]
        path = []
        for key in key_indices:
            path += dict_path[key]
        return path
    else:
        return dict_path[key_index]


def compute_lower_number(key: str, key_numbers: Dict[str, int]):
    value = 0
    for sub_key, number in key_numbers.items():
        if len(key) > len(sub_key):
            if key[0 : len(sub_key)] == sub_key:
                value += number
    return value


def compute_upper_number(key: str, key_numbers: Dict[str, int]):
    value = 0
    for sub_key, number in key_numbers.items():
        if len(key) >= len(sub_key):
            if key[0 : len(sub_key)] == sub_key:
                value += number
    return value


def find_keys(key: str, key_indices: List[str]):
    return [sub_key for sub_key in key_indices if sub_key[0 : len(key)] == key]


def select_direction(
    end_point: Tuple[int, int], neighbours: Dict[str, Tuple[int, int]]
):
    # print(neighbours)
    rev_dict = {coords: move for move, coords in neighbours.items()}
    if end_point in rev_dict:
        return rev_dict[end_point]
    else:
        return random.choice(list(neighbours.keys()))


def create_path_direction_dict(
    directions: Dict[str, Tuple[int, int]], path: List[Tuple[int, int]]
):
    path_dict = {value: move for move, value in directions.items()}
    # transformation of coordinates
    plot_dict = {}
    # build extern function
    for index, tup in enumerate(path):
        if index + 1 < len(path):
            if path[index + 1] not in plot_dict:
                plot_dict[tup] = path_dict[subtract_tuples(path[index + 1], tup)]
            else:
                plot_dict[tup] = "stuck"
    return plot_dict


def remove_coords_from_maze_path(
    maze_path: Dict[int, Dict[str, Tuple[int, int]]],
    current_neighbours: Dict[str, Tuple[int, int]],
) -> None:
    key_list = []
    for values in maze_path.values():
        for key, coords in current_neighbours.items():
            if coords in values:
                key_list.append(key)
    for key in key_list:
        del current_neighbours[key]


def opposite_direction(direction: str):
    opposite_directions = {"up": "down", "down": "up", "right": "left", "left": "right"}
    return opposite_directions[direction]

import os

from typing import Tuple, List


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

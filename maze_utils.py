import os


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


def find_value_in_config(value: float, maze_config: list):
    width = len(maze_config)
    length = len(maze_config[0])
    for i in range(width):
        for j in range(length):
            if value == maze_config[i][j]:
                return True
    return False

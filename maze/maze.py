from abc import ABC, abstractmethod
from cell.cell import Cell
from matplotlib import pyplot as plt
from matplotlib import colors as c
from typing import List, Tuple, Dict
import re
import random
import logging
from maze.maze_utils import (
    verify_file,
    find_value_in_config,
    subtract_tuples,
    transform_coordinates,
    verify_ending,
    transform_single_coordinates,
)


LOG_FILE = "sample.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, "w")
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class InvalidList(Exception):
    pass


class NotSolvable(Exception):
    pass


def full_path(width: int, filename: str = LOG_FILE):
    # verify path
    path_list = []
    with open(filename) as file:
        pattern = re.compile("\((\d+), (\d+)\)")
        for line in file.readlines():
            matches = pattern.finditer(line)
            for match in matches:
                path_list.append((int(match.group(1)), int(match.group(2))))
    if not path_list:
        raise ValueError(
            "The sample.log file is empty. You first need to solve a maze!"
        )
    final_list = []
    for index in range(len(path_list) - 1):
        if path_list[index + 1] != path_list[index]:
            final_list.append(path_list[index])
    final_list.append(path_list[-1])
    return transform_coordinates(final_list, width)


def bfs_full_path(width: int, filename: str = LOG_FILE):
    # verify path
    path_list = []
    with open(filename) as file:
        pattern = re.compile("\((\d+), (\d+)\)")
        for line in file.readlines():
            matches = pattern.finditer(line)
            for match in matches:
                path_list.append((int(match.group(1)), int(match.group(2))))
    if not path_list:
        raise ValueError(
            "The sample.log file is empty. You first need to solve a maze!"
        )
    final_list = []
    for index in range(len(path_list) - 1):
        if path_list[index + 1] != path_list[index]:
            final_list.append(path_list[index])
    final_list.append(path_list[-1])
    return transform_coordinates(final_list, width)


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


def opposite_direction(direction: str):
    opposite_directions = {"up": "down", "down": "up", "right": "left", "left": "right"}
    return opposite_directions[direction]


class Maze:
    valid_values = {1: "C", 0: "W", 2: "S", 3: "E"}
    directions = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

    def __init__(self, maze_config: List[List[int]]):
        self.validate_input(maze_config)
        self.validate_values(maze_config)
        self.config_cells()
        self.init_cell_neighbours()
        self._solution_path = []
        self._full_path = []

    @property
    def solution_path(self):
        if self._solution_path:
            return self._solution_path
        else:
            raise ValueError("The maze has not been solved yet!")

    @property
    def full_path(self):
        if self._full_path:
            return self._full_path
        else:
            raise ValueError("The maze has not been solved yet!")

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    def validate_input(self, maze_config: List[List[int]]):
        try:
            self._length = len(maze_config[0])
            self._width = len(maze_config)
            for i in range(self._length):
                for j in range(self._width):
                    if maze_config[j][i] not in self.valid_values:
                        raise InvalidList()
        except (TypeError, InvalidList):
            raise InvalidList("Provided Inputs do not fit the maze criterion!")

    def validate_values(self, maze_config: List[List[int]]):
        try:
            for value in self.valid_values.keys():
                if not find_value_in_config(value, maze_config):
                    raise InvalidList()
            self.config = maze_config
        except InvalidList:
            raise InvalidList(
                "Either cells, a starting point or an ending point is missing!"
            )

    def config_cells(self):
        self.cell_config = {}
        for i in range(self._length):
            for j in range(self._width):
                typing = self.config[j][i]
                self.cell_config[(j + 1, i + 1)] = Cell(
                    j + 1, i + 1, self.valid_values[typing]
                )
                if typing == 2:
                    self.starting_point = (j + 1, i + 1)
                elif typing == 3:
                    self.ending_point = (j + 1, i + 1)

    def init_cell_neighbours(self):
        for coords, cell in self.cell_config.items():
            x, y = coords
            if cell._typing != "W":
                for key, direction in self.directions.items():
                    x_shift, y_shift = direction
                    if (x + x_shift, y + y_shift) in self.cell_config:
                        if self.cell_config[(x + x_shift, y + y_shift)]._typing != "W":
                            cell._neighbours[key] = (x + x_shift, y + y_shift)

    def __str__(self):
        rep = ""
        for j in range(self._width):
            for i in range(self._length):
                typing = self.config[j][i]
                rep += f"{self.valid_values[typing]:^3}"
            rep += "\n"
        return rep

    def represent_cells(self):
        rep = ""
        for coords, cell in self.cell_config.items():
            x, y = coords
            part_str = f"Cell {(x,y)} has: {len(cell._neighbours)} neighbours! \n"
            part_str += "\n".join(
                f"\t {key} : {neighbour_coords}"
                for key, neighbour_coords in cell._neighbours.items()
            )
            rep += part_str + "\n"
        return rep

    def view_maze(self, path, marker_size=50, pausing=0.01) -> None:
        fig, ax = plt.subplots()
        cmap = c.ListedColormap(["indigo", "darkcyan", "yellow", "lime"])
        ax.pcolormesh([item for item in reversed(self.config)], cmap=cmap)
        ax.yaxis.grid(True, color="black", lw=2.5)
        ax.xaxis.grid(True, color="black", lw=2.5)
        ax.set_xticks(range(self._length))
        ax.set_yticks(range(self._width))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        # plt.axis("off")
        if path:
            plt.pause(2.0)
            direction_dict = {
                "right": "^",
                "left": "v",
                "up": "<",
                "down": ">",
                "stuck": "o",
            }
            for coords, direction in path.items():
                x, y = coords
                # transform coordinates e.g. (5,10) corresponds to (9.5,2.5) on plot
                u, v = (x - 0.5, y - 0.5)
                ax.scatter(
                    x=u,
                    y=v,
                    marker=direction_dict[direction],
                    s=marker_size,
                    c="lightcoral",
                )
                plt.pause(pausing)
        plt.show()
        plt.show()

    def export_maze(self, filename: str = ""):
        if not filename:
            filename = f"maze_examples/maze_{self.length+1}_{self.width+1}.txt"
        verify_ending(filename)
        with open(filename, "w") as file:
            for line in self.config:
                export_str = " ".join(f"{number}" for number in line)
                export_str += "\n"
                file.write(export_str)

    @classmethod
    def import_maze(cls, filename: str, delimiter: str = " "):
        verify_file(filename)
        config = []
        with open(filename, "r") as file:
            try:
                for line in file.readlines():
                    line = line.replace("\n", "")
                    line_config = [int(number) for number in line.split(delimiter)]
                    config.append(line_config)
            except (TypeError, ValueError):
                raise TypeError(
                    "Provided input includes values which cannot be converted to int!"
                )
        return cls(config)


class MazeAlgorithm(ABC):
    @abstractmethod
    def solve(maze: Maze):
        """setting _solution_path and _full_path of the maze"""

    @abstractmethod
    def view_path(
        maze_directions: Dict[str, Tuple[int, int]],
        path: List[Tuple[int, int]],
        choice: str = "",
    ):
        """creates the view of the provided path"""


class MazeSolver:
    def __init__(self, maze: Maze, algorithm: MazeAlgorithm):
        self.maze = maze
        self.algorithm = algorithm
        self._full_path = []
        self._solution_path = []
        self.path_dict = {"full": "_full_path", "solution": "_solution_path"}

    def solve_maze(self):
        solution_path, full_path = self.algorithm.solve(self.maze)
        self._solution_path = solution_path
        self._full_path = full_path

    @property
    def full_path(self):
        return self._full_path

    @property
    def solution_path(self):
        return self._solution_path

    def view_path(
        self, choice: str = "solution", pausing: float = 0.05, marker_size: int = 50
    ) -> None:
        if choice in self.path_dict:
            path = self.__dict__[self.path_dict[choice]]
        else:
            raise ValueError("Invalid Input")
        fig, ax = plt.subplots()
        cmap = c.ListedColormap(["indigo", "darkcyan", "yellow", "lime"])
        ax.pcolormesh([item for item in reversed(self.maze.config)], cmap=cmap)
        ax.yaxis.grid(True, color="black", lw=2.5)
        ax.xaxis.grid(True, color="black", lw=2.5)
        ax.set_xticks(range(self.maze._length))
        ax.set_yticks(range(self.maze._width))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        # plt.axis("off")
        plt.pause(2.0)
        direction_dict = {
            "right": "^",
            "left": "v",
            "up": "<",
            "down": ">",
            "stuck": "o",
        }
        plot_dict = self.algorithm.view_path(self.maze.directions, path, choice)
        for coords, direction in plot_dict.items():
            x, y = coords
            # transform coordinates e.g. (5,10) corresponds to (9.5,2.5) on plot
            u, v = (x - 0.5, y - 0.5)
            ax.scatter(
                x=u,
                y=v,
                marker=direction_dict[direction],
                s=marker_size,
                c="lightcoral",
            )
            plt.pause(pausing)
        plt.show()


class DFSAlgorithm(MazeAlgorithm):
    def solve(maze: Maze):
        return (DFSAlgorithm.get_solution_path(maze), DFSAlgorithm.get_full_path(maze))

    def get_solution_path(maze: Maze):
        with open(LOG_FILE, "w"):
            pass
        start = maze.starting_point
        end = maze.ending_point
        maze_path = {}
        turning_points = []
        index = 0
        current_point = start
        while current_point != end:
            if index in maze_path:
                current_neighbours = maze_path[index][1]
            else:
                current_neighbours = dict(maze.cell_config[current_point]._neighbours)

            remove_coords_from_maze_path(maze_path, current_neighbours)

            if len(current_neighbours) == 0:
                logger.debug(f"Current Point {current_point} has no neighbours!")
                index -= 1
                while index > turning_points[-1]:
                    del maze_path[index]
                    index -= 1
                # index -= 1
                next_point = maze_path[index][0]
                index -= 1

            elif len(current_neighbours) == 1:
                if index in turning_points:
                    turning_points.remove(index)
                # key = random.choice(list(current_neighbours.keys()))
                key = select_direction(end, current_neighbours)
                # check if neighbour is end_point
                next_point = current_neighbours[key]
                logger.debug(
                    f"Current Point {current_point} has 1 neighbour! Next Point {next_point}"
                )
                del current_neighbours[key]
                maze_path[index] = [
                    current_point,
                    current_neighbours,
                ]
            else:
                if index not in turning_points:
                    turning_points.append(index)
                # key = random.choice(list(current_neighbours.keys()))
                key = select_direction(end, current_neighbours)
                # check if neighbour is end_point
                next_point = current_neighbours[key]
                logger.debug(
                    f"Current Point {current_point} has at least 2 neighbours! Next Point {next_point}"
                )
                del current_neighbours[key]
                maze_path[index] = [
                    current_point,
                    current_neighbours,
                ]
            current_point = next_point
            index += 1

        path = [values[0] for values in maze_path.values()]
        path.append(end)
        return transform_coordinates(path, maze.width)

    def get_full_path(maze: Maze):
        path_list = []
        with open(LOG_FILE) as file:
            pattern = re.compile("\((\d+), (\d+)\)")
            for line in file.readlines():
                matches = pattern.finditer(line)
                for match in matches:
                    path_list.append((int(match.group(1)), int(match.group(2))))
        if not path_list:
            raise ValueError(
                "The sample.log file is empty. You first need to solve a maze!"
            )
        final_list = []
        for index in range(len(path_list) - 1):
            if path_list[index + 1] != path_list[index]:
                final_list.append(path_list[index])
        final_list.append(path_list[-1])
        return transform_coordinates(final_list, maze.width)

    def view_path(
        maze_directions: Dict[str, Tuple[int, int]],
        path: List[Tuple[int, int]],
        choice: str = "",
    ):
        path_dict = {value: move for move, value in maze_directions.items()}
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


def dfs_algorithm(maze: Maze):
    with open(LOG_FILE, "w"):
        pass
    start = maze.starting_point
    end = maze.ending_point
    maze_path = {}
    turning_points = []
    index = 0
    current_point = start
    while current_point != end:
        if index in maze_path:
            current_neighbours = maze_path[index][1]
        else:
            current_neighbours = dict(maze.cell_config[current_point]._neighbours)

        remove_coords_from_maze_path(maze_path, current_neighbours)

        if len(current_neighbours) == 0:
            logger.debug(f"Current Point {current_point} has no neighbours!")
            index -= 1
            while index > turning_points[-1]:
                del maze_path[index]
                index -= 1
            # index -= 1
            next_point = maze_path[index][0]
            index -= 1

        elif len(current_neighbours) == 1:
            if index in turning_points:
                turning_points.remove(index)
            # key = random.choice(list(current_neighbours.keys()))
            key = select_direction(end, current_neighbours)
            # check if neighbour is end_point
            next_point = current_neighbours[key]
            logger.debug(
                f"Current Point {current_point} has 1 neighbour! Next Point {next_point}"
            )
            del current_neighbours[key]
            maze_path[index] = [
                current_point,
                current_neighbours,
            ]
        else:
            if index not in turning_points:
                turning_points.append(index)
            # key = random.choice(list(current_neighbours.keys()))
            key = select_direction(end, current_neighbours)
            # check if neighbour is end_point
            next_point = current_neighbours[key]
            logger.debug(
                f"Current Point {current_point} has at least 2 neighbours! Next Point {next_point}"
            )
            del current_neighbours[key]
            maze_path[index] = [
                current_point,
                current_neighbours,
            ]
        current_point = next_point
        index += 1

    path = [values[0] for values in maze_path.values()]
    path.append(end)
    return path


def bfs_algorithm(maze: Maze):
    with open(LOG_FILE, "w"):
        pass
    start = maze.starting_point
    end = maze.ending_point
    search_loop = True
    dict_path: dict = {"1": [start]}
    dict_active: dict = {"1": start}
    current_point = start
    while search_loop:
        for key_index in dict_active.copy().keys():
            current_point = dict_active[key_index]
            current_neighbours = dict(maze.cell_config[current_point]._neighbours)
            # remove_coords_from_maze_path(maze_path, current_neighbours)

            if len(current_neighbours) == 0:
                del dict_active[key_index]
                if not dict_active:
                    raise NotSolvable("Maze is not solvable!")

            elif len(current_neighbours) == 1:
                direction = select_direction(end, current_neighbours)
                next_point = current_neighbours[direction]
                logger.debug(
                    f"Current Point {current_point} has 1 neighbour! Next Point {next_point}"
                )
                dict_path[key_index].append(next_point)
                if next_point == end:
                    search_loop = False
                    break
                dict_active[key_index] = next_point
                del maze.cell_config[next_point]._neighbours[
                    opposite_direction(direction)
                ]

            else:
                logger.debug(
                    f"Current Point {current_point} has at least 2 neighbours! Path will be split"
                )
                for index, direction in enumerate(current_neighbours.copy().keys()):
                    next_point = current_neighbours[direction]
                    if next_point == end:
                        search_loop = False
                        dict_path[key_index].append(next_point)
                        break

                    del maze.cell_config[next_point]._neighbours[
                        opposite_direction(direction)
                    ]
                    dict_active[key_index + "." + str(index + 1)] = next_point
                    dict_path[key_index + "." + str(index + 1)] = [next_point]
                del dict_active[key_index]

    path = construct_bfs_path(key_index, dict_path)
    print(dict_path)
    return transform_coordinates(path, maze.width)


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


def view_solution_path(
    maze_directions: Dict[str, Tuple[int, int]], path: List[Tuple[int, int]]
):
    path_dict = {value: move for move, value in maze_directions.items()}
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


def view_full_path(
    maze_directions: Dict[str, Tuple[int, int]], path: List[Tuple[int, int]]
):
    path_dict = {value: move for move, value in maze_directions.items()}
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


def view_path(
    maze_directions: Dict[str, Tuple[int, int]],
    path: List[Tuple[int, int]],
    choice: str = "",
):
    path_dict = {value: move for move, value in maze_directions.items()}
    key_indices = list(path.keys())
    key_relationship = {key: find_keys(key, key_indices) for key in key_indices}
    key_numbers = {key: len(path[key]) for key in key_indices}
    total_lower_key_numbers = {
        key: compute_lower_number(key, key_numbers) for key in key_numbers
    }
    total_upper_key_numbers = {
        key: compute_upper_number(key, key_numbers) for key in key_numbers
    }
    min_value = 0
    max_value = max(list(total_upper_key_numbers.values()))
    final_path = {}
    for index in range(min_value, max_value):
        for key in key_numbers:
            key_min_val, key_max_val = (
                total_lower_key_numbers[key],
                total_upper_key_numbers[key],
            )
            if key_min_val <= index and key_max_val > index:
                coords = path[key][index - key_min_val]
                if index + 1 == key_max_val:
                    sign = "stuck"
                else:
                    sign = path_dict[
                        subtract_tuples(path[key][index - key_min_val + 1], coords)
                    ]
                final_path[transform_single_coordinates(coords, 11)] = sign
    return final_path


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


class Tree:
    def __init__(self, path):
        key_indices = list(path.keys())


class Node:
    def __init__(self, children, tuple_list):
        self.tuples = tuple_list
        self.children = children


# view_path_solution / #view_path_full


def construct_bfs_full_path(dict_path: Dict[str, List[Tuple[int, int]]]):
    pass


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

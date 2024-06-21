from typing import Tuple, Dict, List
from maze.maze import Maze, logger, LOG_FILE
from matplotlib import pyplot as plt
from matplotlib import colors as c
from abc import ABC, abstractmethod
from maze.maze_utils import (
    subtract_tuples,
    transform_coordinates,
    remove_coords_from_maze_path,
    select_direction,
    opposite_direction,
    compute_lower_number,
    compute_upper_number,
    construct_bfs_path,
)

import re


class NotSolvable(Exception):
    pass


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
        plot_dict[path[-1]] = "stuck"
        return plot_dict


class BFSAlgorithm(MazeAlgorithm):
    def solve(maze: Maze):
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
        dict_path = {
            key: transform_coordinates(value, maze.width)
            for key, value in dict_path.items()
        }
        return (transform_coordinates(path, maze.width), dict_path)

    def view_path(
        maze_directions: Dict[str, Tuple[int, int]],
        path: List[Tuple[int, int]],
        choice: str = "",
    ):
        if choice == "solution":
            return BFSAlgorithm.view_solution_path(maze_directions, path)
        elif choice == "full":
            return BFSAlgorithm.view_full_path(maze_directions, path)
        else:
            raise ValueError("BFS: Invalid Input!")

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
        plot_dict[path[-1]] = "stuck"
        return plot_dict

    def view_full_path(
        maze_directions: Dict[str, Tuple[int, int]],
        path: List[Tuple[int, int]],
    ):
        path_dict = {value: move for move, value in maze_directions.items()}
        key_indices = list(path.keys())
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
                    final_path[coords] = sign
        return final_path

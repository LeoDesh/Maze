from cell import Cell
from matplotlib import pyplot as plt
import random
import logging

LOG_FILE = "sample.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, "w")
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class InvalidList(Exception):
    pass


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


class Maze:
    valid_values = {1: "C", 0: "W", 0.25: "S", 0.75: "E"}
    directions = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

    def __init__(self, maze_config: list):
        self.validate_input(maze_config)
        self.validate_values(maze_config)
        self.config_cells()
        self.init_cell_neighbours()

    def validate_input(self, maze_config: list):
        try:
            self._length = len(maze_config[0])
            self._width = len(maze_config)
            for i in range(self._length):
                for j in range(self._width):
                    if maze_config[j][i] not in self.valid_values:
                        raise InvalidList()
        except (TypeError, InvalidList):
            raise InvalidList("Provided Inputs do not fit the maze criterion!")

    def validate_values(self, maze_config: list):
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
                if typing == 0.25:
                    self.starting_point = (j + 1, i + 1)
                elif typing == 0.75:
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

    def matplotlib_view(self, path: list = None) -> None:
        fig, ax = plt.subplots()
        ax.pcolormesh([item for item in reversed(self.config)])
        ax.yaxis.grid(True, color="black", lw=2.5)
        ax.xaxis.grid(True, color="black", lw=2.5)
        ax.set_xticks(range(self._length))
        ax.set_yticks(range(self._width))
        if path:
            plt.pause(2.0)
            path_dict = {value: move for move, value in self.directions.items()}
            direction_dict = {"right": ">", "left": "<", "up": "^", "down": "v"}
            plot_dict = {}
            for index, tup in enumerate(path):
                if index + 1 < len(path):
                    plot_dict[tup] = path_dict[subtract_tuples(path[index + 1], tup)]
            for coords, direction in plot_dict.items():
                x, y = coords
                # transform coordinates e.g. (5,10) corresponds to (9.5,2.5) on plot
                u, v = (y - 0.5), (self._width - x + 0.5)
                ax.scatter(
                    x=u, y=v, marker=direction_dict[direction], s=65, c="lightcoral"
                )
                plt.pause(0.05)
        plt.show()


class MazeSolver:
    def __init__(self, maze: Maze, algorithm):
        self.maze = maze
        self.algorithm = algorithm

    def solve_maze(self):
        return self.algorithm(self.maze)


def dfs_algorithm(maze: Maze):
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
            key = random.choice(list(current_neighbours.keys()))
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
            key = random.choice(list(current_neighbours.keys()))
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


def remove_coords_from_maze_path(maze_path: dict, current_neighbours: dict) -> None:
    key_list = []
    for values in maze_path.values():
        for key, coords in current_neighbours.items():
            if coords in values:
                key_list.append(key)
    for key in key_list:
        del current_neighbours[key]

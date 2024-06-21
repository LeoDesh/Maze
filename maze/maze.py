from cell.cell import Cell
from matplotlib import pyplot as plt
from matplotlib import colors as c
from typing import List
import logging
from maze.maze_utils import (
    verify_file,
    find_value_in_config,
    verify_ending,
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


""" def full_path(width: int, filename: str = LOG_FILE):
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
    return transform_coordinates(final_list, width) """


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

    def view_maze(self) -> None:
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

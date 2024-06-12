from abc import abstractmethod
from abc import ABC
from cell import Cell
import random
import logging

LOG_FILE = "sample_factory.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, "w")
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def add_tuples(t1: tuple, t2: tuple):
    return tuple(s + t for s, t in zip(t1, t2))


def update_turning_points(turning_points, visited_cells, cells_neighbours):
    for point in list(turning_points):
        index = 0
        neighbour_list = cells_neighbours[point]._neighbours
        size = len(neighbour_list)
        for key, value in dict(neighbour_list).items():
            if value in visited_cells:
                index += 1
                del neighbour_list[key]
        if size == index:
            turning_points.remove(point)


def inverse_move(move: str):
    if move == "up":
        return "down"
    elif move == "down":
        return "up"
    elif move == "right":
        return "left"
    elif move == "left":
        return "right"
    else:
        raise ValueError(f"{move} is an invalid input!")


class MazeFactory(ABC):
    directions = {"up": (-2, 0), "down": (2, 0), "right": (0, 2), "left": (0, -2)}
    wall_directions = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

    def __init__(self, width: int, length: int):
        self._width = width
        self._length = length

    @abstractmethod
    def create_maze(self) -> list:
        """Implementation of a maze as a lists of 0 and 1"""


class DFSMaze(MazeFactory):
    def __init__(self, width: int, length: int):
        super().__init__(width, length)
        self._cells = {
            (2 * i + 1, 2 * j + 1): Cell(2 * i + 1, 2 * j + 1, "C")
            for i in range(width)
            for j in range(length)
        }
        self._walls = {
            (i + 1, j + 1): Cell(i + 1, j + 1, "W")
            for i in range(2 * width - 1)
            for j in range(2 * length - 1)
            if (i + 1, j + 1) not in self._cells
        }
        self._visited_cells = []
        self.init_cell_neighbours()

    def create_maze(self) -> list:
        key = random.choice(list(self._cells.keys()))
        total_amount = self._width * self._length
        current_point = key
        turning_points = []
        # print(list(self._cells.keys()))
        # print(list(self._walls.keys()))
        while len(self._visited_cells) < total_amount - 1:
            # delete the current point out of the neighbours
            size = len(self._cells[current_point]._neighbours.items())
            for move, coords in self._cells[current_point]._neighbours.items():
                if inverse_move(move) in self._cells[coords]._neighbours.keys():
                    del self._cells[coords]._neighbours[inverse_move(move)]

            if size == 0:
                next_point = turning_points[-1]
                turning_points.remove(turning_points[-1])
                logger.debug(
                    f"Current Point {current_point} has 0 neighbour! Next Point {next_point}"
                )
            elif size == 1:
                if current_point in turning_points:
                    turning_points.remove(current_point)
                next_point = self.update_step(current_point)
                self._visited_cells.append(next_point)
                logger.debug(
                    f"Current Point {current_point} has 1 neighbour! Next Point {next_point}"
                )
            else:
                if current_point not in turning_points:
                    turning_points.append(current_point)

                next_point = self.update_step(current_point)
                self._visited_cells.append(next_point)
                logger.debug(
                    f"Current Point {current_point} has more than 1 neighbour! Next Point {next_point}"
                )

            current_point = next_point
            update_turning_points(turning_points, self._visited_cells, self._cells)

        return self.maze_list()

    def update_step(self, current_point: tuple) -> tuple:
        key = random.choice(list(self._cells[current_point]._neighbours.keys()))
        next_point = self._cells[current_point]._neighbours[key]
        wall_point = add_tuples(current_point, self.wall_directions[key])
        self._cells[wall_point] = self._walls[wall_point]
        del self._walls[wall_point]
        del self._cells[current_point]._neighbours[key]
        return next_point

    def init_cell_neighbours(self) -> None:
        for coords, cell in self._cells.items():
            for key, move in self.directions.items():
                if add_tuples(coords, move) in self._cells:
                    cell._neighbours[key] = add_tuples(coords, move)

    def maze_list(self) -> list:
        maze = [
            [-1 for _ in range(2 * self._length - 1)]
            for _ in range(2 * self._width - 1)
        ]
        for coords in self._cells.keys():
            i, j = coords
            maze[i - 1][j - 1] = 1
        for coords in self._walls.keys():
            i, j = coords
            maze[i - 1][j - 1] = 0
        starting_point = random.choice(list(self._cells.keys()))
        i, j = starting_point
        maze[i - 1][j - 1] = 0.25
        end_point = random.choice(list(self._cells.keys()))
        i, j = end_point
        maze[i - 1][j - 1] = 0.75
        return maze

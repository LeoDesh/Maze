from maze.maze import Maze, MazeSolver, dfs_algorithm, full_path
from maze.maze_factory import DFSMaze
from typing import Tuple
# import random


def read_maze(filename: str = "maze_examples/maze_24_16.txt") -> Maze:
    """Reads maze from file"""
    return Maze.import_maze(filename)


def create_maze(width: int = 10, length: int = 20):
    """Generates a random maze with provided sizes"""
    maze_generator = DFSMaze(width, length)
    maze_generator.create_maze()
    maze_list = maze_generator.maze
    return Maze(maze_list)


def solve_maze(maze: Maze) -> Tuple[int, int]:
    solver = MazeSolver(maze, dfs_algorithm)
    return solver.solve_maze()


def plot_solution_path(
    maze: Maze,
    solution_path: Tuple[int, int],
    pausing: float = 0.0005,
    marker_size: int = 20,
) -> None:
    maze.matplotlib_view(path=solution_path, pausing=pausing, marker_size=marker_size)


# full_path


def plot_full_algorithm_path(
    maze: Maze,
    pausing: float = 0.0005,
    marker_size: int = 20,
) -> None:
    maze.matplotlib_view(
        path=full_path(maze.width), pausing=pausing, marker_size=marker_size
    )


def main():
    ## 1) Create Mazes
    ## 1a) read_maze via files
    # maze = read_maze()

    ## 1b) create_maze via parameters
    maze = create_maze(length=20, width=15)

    ## 2) Solve Maze
    solution_path = solve_maze(maze=maze)

    ## 3) Plot Maze
    # 3a) plot solution path
    plot_solution_path(maze, solution_path)

    # 3b) plot all visited cells
    # plot_full_algorithm_path(maze)

    ## 4) Export Maze
    ## 0-Walls / 1-Cells / 2-Start / 3-End
    # maze.export_maze()


if __name__ == "__main__":
    main()

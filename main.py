from maze.maze import Maze, MazeSolver, dfs_algorithm
from maze.maze_factory import DFSMaze
from pathlib import Path
import random


def read_maze(filename: str = "maze_examples/maze_60_40.txt"):
    maze = Maze.import_maze("maze_examples/maze_60_40.txt")
    solver = MazeSolver(maze, dfs_algorithm)
    path = solver.solve_maze()
    maze.matplotlib_view(path=path, pausing=0.0005, marker_size=20)


def maze_example(width: int = 10, length: int = 20):
    maze_generator = DFSMaze(width, length)
    maze_generator.create_maze()
    maze_list = maze_generator.maze
    maze = Maze(maze_list)
    solver = MazeSolver(maze, dfs_algorithm)
    path = solver.solve_maze()
    maze.matplotlib_view(path=path, pausing=0.001, marker_size=40)


def main():
    ## read_maze via files

    # read_maze()

    ## generate own maze with provided length and width (e.g. 20 and 10)

    # maze_example()
    pass


if __name__ == "__main__":
    main()

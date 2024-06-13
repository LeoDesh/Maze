from maze.maze import Maze, MazeSolver, dfs_algorithm
from maze.maze_factory import DFSMaze
from pathlib import Path
import random


""" 
random.seed(4)
    maze = get_maze_text()
    # maze = [[1, 1, 0], [0, 0.5, 1], [1, 1, 0]]
    width = 4
    length = 6
    maze_generator = DFSMaze(width, length)
    maze_list = maze_generator.create_maze()
    maze = Maze(maze_list)

 """

""" 
Config long maze:
random.seed(15)
    width = 20
    length = 40

    width = 30
    length = 60

 """


def main():
    """random.seed(15)
    width = 40
    length = 60
    # maze = get_maze_text()
    # maze = [[1, 1, 0], [0, 0.5, 1], [1, 1, 0]]

    maze_generator = DFSMaze(width, length)
    maze_generator.create_maze()
    maze_list = maze_generator.maze"""
    maze = Maze.import_maze("maze_examples/maze_60_40.txt")
    solver = MazeSolver(maze, dfs_algorithm)
    path = solver.solve_maze()
    maze.matplotlib_view(path=path, pausing=0.001, marker_size=30)
    # maze_generator.export_maze("maze_examples/maze_60_40.txt")


if __name__ == "__main__":
    main()

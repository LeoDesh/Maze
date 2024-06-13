from maze import Maze, MazeSolver, dfs_algorithm
from maze_factory import DFSMaze
import random
from pathlib import Path


def get_maze_text():
    maze = []
    with open("maze.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            row = []
            for c in line:
                if c == " ":
                    row.append(1)  # spaces are 1s
                else:
                    row.append(0)  # walls are 0s
            maze.append(row)
    return maze


def generate_maze(length: int, width: int):
    pass


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


def process_path(path: str, relative_backwards: str):
    folders = path.split("\\")
    count = relative_backwards.count(".")
    return "\\".join(folders[i] for i in range(len(folders) - count))


def main():
    random.seed(15)
    width = 30
    length = 60
    # maze = get_maze_text()
    # maze = [[1, 1, 0], [0, 0.5, 1], [1, 1, 0]]

    """ maze_generator = DFSMaze(width, length)
    maze_list = maze_generator.create_maze()
    maze = Maze(maze_list)
    solver = MazeSolver(maze, dfs_algorithm)
    path = solver.solve_maze()
    maze.matplotlib_view(path) """
    path = str(Path().absolute())
    print("Directory Path:", Path().absolute())
    print(process_path(path, "."))


if __name__ == "__main__":
    main()

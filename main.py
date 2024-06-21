from maze.maze import Maze
from maze.algorithm import DFSAlgorithm, BFSAlgorithm, MazeSolver
from maze.maze_factory import DFSMaze


def read_maze(filename: str = "maze_examples/maze_24_16.txt") -> Maze:
    """Reads maze from file"""
    return Maze.import_maze(filename)


def plot_maze(maze: Maze) -> None:
    """Plot a maze"""
    maze.view_maze()


def create_maze(width: int = 10, length: int = 20):
    """Generates a random maze with provided sizes"""
    maze_generator = DFSMaze(width, length)
    maze_generator.create_maze()
    maze_list = maze_generator.maze
    return Maze(maze_list)


def solve_maze(maze: Maze, algorithm=DFSAlgorithm) -> None:
    solver = MazeSolver(maze, algorithm)
    solver.solve_maze()


def plot_solution_path(
    solver: MazeSolver,
    pausing: float = 0.0005,
    marker_size: int = 20,
) -> None:
    solver.view_path(choice="solution", pausing=pausing, marker_size=marker_size)
    # maze.matplotlib_view(path=solution_path, pausing=pausing, marker_size=marker_size)


# full_path


def plot_full_algorithm_path(
    solver: MazeSolver,
    pausing: float = 0.0005,
    marker_size: int = 20,
) -> None:
    solver.view_path(choice="full", pausing=pausing, marker_size=marker_size)


def main():
    ## 1) Create Mazes
    ## 1a) read_maze via files
    maze = read_maze("maze_examples/maze_24_16.txt")

    ## 1b) create_maze via parameters
    # maze = read_maze("maze_examples/maze_60_40.txt")

    ## 2) Solve Maze
    # Select algorithm (DFSAlgorithm or BFSAlgorithm)

    maze_solver = MazeSolver(maze=maze, algorithm=DFSAlgorithm)
    maze_solver.solve_maze()

    ## 3) Plot Maze
    # 3a) plot solution path
    # plot_solution_path(maze_solver)

    # 3b) plot all visited cells
    plot_full_algorithm_path(maze_solver)

    ## 4) Export Maze
    ## 0-Walls / 1-Cells / 2-Start / 3-End
    # maze.export_maze("tests/maze_examples/maze_6_3.txt")


if __name__ == "__main__":
    main()

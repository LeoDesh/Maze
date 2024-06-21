from maze.maze import (
    Maze,
    InvalidList,
)
from maze.maze_utils import find_value_in_config
from maze.algorithm import DFSAlgorithm, MazeSolver
import pytest


@pytest.fixture
def example_maze():
    return Maze.import_maze("tests/maze_examples/maze_12_6.txt")


@pytest.fixture
def example_sample_full_path():
    return [
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 3),
        (3, 3),
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 11),
        (4, 11),
        (3, 11),
        (3, 10),
    ]


@pytest.fixture
def example_fail_list():
    return [1, 2, 5]


@pytest.fixture
def example_fail_values_list():
    return [[0, 1, 5], [2, 1, 1]]


@pytest.fixture
def example_pass_list():
    return [[0, 2], [1, 3]]


@pytest.fixture
# maze_12_6.txt
def solution_path():
    return [
        (9, 4),
        (9, 5),
        (10, 5),
        (11, 5),
        (11, 4),
        (11, 3),
        (11, 2),
        (11, 1),
        (10, 1),
        (9, 1),
        (8, 1),
        (7, 1),
        (6, 1),
    ]


def test_validate_values_1(example_pass_list):
    assert find_value_in_config(3, example_pass_list)


def test_validate_values_2(example_pass_list):
    assert not find_value_in_config(5, example_pass_list)


def test_validate_input_1(example_maze, example_fail_values_list):
    with pytest.raises(InvalidList):
        example_maze.validate_input(example_fail_values_list)


def test_validate_input_2(example_maze, example_pass_list):
    example_maze.validate_input(example_pass_list)
    assert example_maze.width == 2 and example_maze.length == 2


def test_validate_input_3(example_maze, example_fail_list):
    with pytest.raises(InvalidList):
        example_maze.validate_input(example_fail_list)


def test_validate_values(example_maze, example_fail_values_list):
    with pytest.raises(InvalidList):
        example_maze.validate_input(example_fail_values_list)


def test_config_cells_starting_point(example_maze):
    assert example_maze.starting_point == (2, 9)


def test_config_cells_end_point(example_maze):
    assert example_maze.ending_point == (5, 6)


def test_maze_solver_dfs(example_maze, solution_path):
    maze_solver = MazeSolver(example_maze, DFSAlgorithm)
    maze_solver.solve_maze()
    assert maze_solver.solution_path == solution_path


def test_import_maze(example_maze):
    with pytest.raises(TypeError):
        example_maze.import_maze("tests/maze_examples/maze_fail.txt")


# export_maze, split part of matplotview, put single functions in utils file

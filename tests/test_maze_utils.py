import pytest
from maze.maze_utils import (
    transform_coordinates,
    retransform_coordinates,
    add_tuples,
    subtract_tuples,
    verify_ending,
    verify_file,
    find_value_in_config,
)

width = 5


@pytest.fixture
def tuple_1():
    return (1, 2)


@pytest.fixture
def tuple_2():
    return (2, 1)


@pytest.fixture
def tuple_list():
    return [(i, i + 1) for i in range(10)]


@pytest.fixture
def list_list():
    return [[i + 1 for i in range(10)] for j in range(6)]


def test_add_tuples(tuple_1, tuple_2):
    assert add_tuples(tuple_1, tuple_2) == (3, 3)


def test_substract_tuples(tuple_1, tuple_2):
    assert subtract_tuples(tuple_1, tuple_2) == (-1, 1)


def test_transform_coordinates(tuple_list):
    width = 5
    assert (
        retransform_coordinates(transform_coordinates(tuple_list, width), width)
        == tuple_list
    )


def test_retransform_coordinates(tuple_list):
    width = 5
    assert (
        transform_coordinates(retransform_coordinates(tuple_list, width), width)
        == tuple_list
    )


def test_verify_ending():
    with pytest.raises(TypeError):
        verify_ending("main.py")


def test_verify_file_1():
    with pytest.raises(TypeError):
        verify_file("main.py")


def test_verify_file_2():
    with pytest.raises(ValueError):
        verify_file("maze_examples")


def test_find_value_in_config_1(list_list):
    assert find_value_in_config(5, list_list)


def test_find_value_in_config_2(list_list):
    assert not find_value_in_config(12, list_list)

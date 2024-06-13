import pytest
from ..cell.cell import Cell

X_1 = 1
Y_1 = 1
X_2 = 4
Y_2 = 5


@pytest.fixture
def cell_1():
    return Cell(X_1, Y_1, "W")


def test_cell_getters(cell_1):
    assert X_1 == cell_1.x


def test_cell_setters(cell_1):
    cell_1.y = 5
    assert Y_2 == cell_1.y


def test_cell_setters_negative_values(cell_1):
    with pytest.raises(ValueError):
        cell_1.y = -5


def test_cell_setters_string_values(cell_1):
    with pytest.raises(TypeError):
        cell_1.y = "hi"

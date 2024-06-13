class Cell:
    def __init__(self, x: int, y: int, typing: str):
        self._x = x
        self._y = y
        self._typing = typing
        self._neighbours = {}

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x_value: int):
        if not isinstance(x_value, int):
            raise TypeError(f"Provided value: {x_value} has the wrong type!")
        elif x_value <= 0:
            raise ValueError(f"Provided value: {x_value} must not be negative or 0!")
        self._x = x_value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y_value: int):
        if not isinstance(y_value, int):
            raise TypeError(f"Provided value: {y_value} has the wrong type!")
        elif y_value <= 0:
            raise ValueError(f"Provided value: {y_value} must not be negative or 0!")
        self._y = y_value

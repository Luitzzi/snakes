from enum import Enum


# ClassTypes
class TSize:
    w: int
    h: int

    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h


class TPos:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def flat(self) -> tuple[int, int]:
        return (self.x, self.y)


# Enums
class Direction(Enum):
    """
    The direction in that the snake can move.
    For consistency implement them in the following order:
    -> North, east, south, west
    """

    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)

    def __getitem__(self, index):
        return self.value[index]

    def val(self):
        return self.value


class Collision(Enum):
    BODY = (0, 0)
    CURVE = (1, 1)
    TAIL = (-1, -1)
    LEFT = (-1, 0)
    TOP = (0, -1)
    RIGHT = (1, 0)
    BOTTOM = (0, 1)

    def val(self):
        return self.value

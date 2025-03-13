from enum import Enum


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


def is_opposite_dir(direction1, direction2):
    match direction1:
        case Direction.NORTH:
            return direction2 == Direction.SOUTH
        case Direction.EAST:
            return direction2 == Direction.WEST
        case Direction.SOUTH:
            return direction2 == Direction.NORTH
        case Direction.WEST:
            return direction2 == Direction.EAST


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

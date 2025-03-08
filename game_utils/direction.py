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

def add_position_tuples(a, b):
    """
    Add two tuples with two values
    :return: Resulting tuple from the addition
    """
    return (a[0] + b[0], a[1] + b[1])

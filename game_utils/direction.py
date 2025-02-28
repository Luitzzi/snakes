from enum import Enum

class Direction(Enum):
    """
    The direction in that the snake can move.
    For consistency implement them in the following order:
    -> North, east, south, west
    """
    NORTH = (-1, 0)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (0, -1)

    def __getitem__(self, index):
        return self.value[index]

from enum import Enum


class Direction(Enum):
    left = (-1, 0)
    right = (1, 0)
    up = (0, -1)
    down = (0, 1)

    def __getitem__(self, index):
        return self.value[index]

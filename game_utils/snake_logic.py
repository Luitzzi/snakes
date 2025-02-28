import config
from game_utils.direction import Direction


class SnakeLogic:
    default_direction = config.SNAKE_DEFAULT_DIRECTION
    starting_position = config.SNAKE_STARTING_POSITION

    def __init__(self):
        self.body = self.starting_position
        self.direction = self.default_direction

    def set_direction(self, new_direction):
        match new_direction:
            case Direction.NORTH:
                if self.direction != Direction.EAST:
                    self.direction = Direction.NORTH
            case Direction.EAST:
                if self.direction != Direction.NORTH:
                    self.direction = Direction.EAST
            case Direction.WEST:
                if self.direction != Direction.SOUTH:
                    self.direction = Direction.WEST
            case Direction.SOUTH:
                if self.direction != Direction.WEST:
                    self.direction = Direction.SOUTH

    def get_head(self):
        return self.body[0]

    def move(self):
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)
        return new_head

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

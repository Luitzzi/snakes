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
            case Direction.left:
                if self.direction != Direction.right:
                    self.direction = Direction.left
            case Direction.right:
                if self.direction != Direction.left:
                    self.direction = Direction.right
            case Direction.up:
                if self.direction != Direction.down:
                    self.direction = Direction.up
            case Direction.down:
                if self.direction != Direction.up:
                    self.direction = Direction.down

    def move(self):
        """
        Moves the snake in the direction that is saved in self.direction.
        Return the position of the new_head for collision checking.
        :return: new_head position
        """
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)
        return new_head

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

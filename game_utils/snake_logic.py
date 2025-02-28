import config
from game_utils.direction import is_opposite_dir


class SnakeLogic:
    default_direction = config.SNAKE_DEFAULT_DIRECTION
    starting_position = config.SNAKE_STARTING_POSITION

    def __init__(self):
        self.body = self.starting_position
        self.direction = self.default_direction
        self.new_direction = self.default_direction

    def set_direction(self, new_direction):
        if not is_opposite_dir(self.direction, new_direction):
            print(f"True {self.new_direction} - {new_direction}")
            self.new_direction = new_direction
        else:
            print(f"False {self.direction} - {new_direction}")

    def get_head(self):
        return self.body[0]

    def move(self):
        self.direction = self.new_direction
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)
        return new_head

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

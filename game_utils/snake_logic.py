import config
from game_utils.direction import is_opposite_dir
from sprites.sprite_utils import WIGGLE_L


class SnakeLogic:
    default_direction = config.SNAKE_DEFAULT_DIRECTION

    def __init__(self, starting_position):
        # copies the list, so the one from config is not modified when modifying body
        self.body = list(starting_position)
        self.prev_direction = self.default_direction
        self.direction = self.default_direction
        self.new_direction = self.default_direction
        self.next_new_direction = self.default_direction
        self.wiggle_offset = WIGGLE_L
        self.collided_with = None

    def set_direction(self, direction):
        if self.direction == self.new_direction:
            if not is_opposite_dir(self.direction, direction):
                self.next_new_direction = self.new_direction = direction
        else:
            if not is_opposite_dir(self.new_direction, direction):
                self.next_new_direction = direction

    def get_head(self):
        return self.body[0]

    def remove_head(self):
        self.body.pop(0)

    def move(self):
        self.prev_direction = self.direction
        self.direction = self.new_direction
        self.new_direction = self.next_new_direction
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)
        # change wiggle side
        self.wiggle_offset = 1 - self.wiggle_offset
        return new_head

    def collide(self, obstacle):
        self.collided_with = obstacle

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

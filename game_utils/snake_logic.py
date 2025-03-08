import config
from game_utils.direction import is_opposite_dir


class SnakeLogic:
    default_direction = config.SNAKE_DEFAULT_DIRECTION

    def __init__(self, starting_position):
        # copies the list, so the one from config is not modified when modifying body
        self.body = list(starting_position)
        self.direction = self.default_direction
        self.new_direction = self.default_direction
        self.next_new_direction = self.default_direction

    def set_direction(self, direction):
        if self.direction == self.new_direction:
            if not is_opposite_dir(self.direction, direction):
                self.next_new_direction = self.new_direction = direction
        else:
            print("a")
            if not is_opposite_dir(self.new_direction, direction):
                self.next_new_direction = direction
                print("b")

    def get_head(self):
        return self.body[0]

    def move(self):
        self.direction = self.new_direction
        self.new_direction = self.next_new_direction
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)
        return new_head

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

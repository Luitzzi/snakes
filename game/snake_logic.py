import config
from gui.sprites.sprite_utils import WIGGLE_L
from defs import Direction, TPos


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
        self.food_pos: TPos = None

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

    def set_food_pos(self, food_pos: TPos) -> None:
        self.food_pos = food_pos

    def get_food_pos(self) -> TPos:
        return self.food_pos

    def is_food_ahead(self) -> bool:
        next_head = self.calc_new_head(self.new_direction)
        return next_head == self.food_pos or self.get_head() == self.food_pos

    def move(self):
        self.prev_direction = self.direction
        self.direction = self.new_direction
        self.new_direction = self.next_new_direction
        new_head = self.calc_new_head(self.direction)
        self.body.insert(0, new_head)
        # change wiggle side
        self.wiggle_offset = 1 - self.wiggle_offset
        return new_head

    def collide(self, obstacle):
        self.collided_with = obstacle

    def calc_new_head(self, direction):
        new_head = (
            self.body[0][0] + direction[0],
            self.body[0][1] + direction[1],
        )
        return new_head


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

import config
import utils
from game_utils.direction import Direction


class Snake:
    default_direction = Direction.right

    def __init__(self):
        self.body = [
            (config.WIDTH // 2, config.HEIGHT // 2),
            (config.WIDTH // 2 - 1, config.HEIGHT // 2),
        ]
        self.direction = self.default_direction

    def draw(self, screen):
        for segment in self.body:
            print("Drawing: x={}; y={}".format(segment[0], segment[1]))
            utils.draw_tile(screen, segment[0], segment[1], config.SNAKE_COLOR)

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
        new_head = self.__calc_new_head()
        self.body.insert(0, new_head)

    def __calc_new_head(self):
        new_head = (
            self.body[0][0] + self.direction[0],
            self.body[0][1] + self.direction[1],
        )
        return new_head

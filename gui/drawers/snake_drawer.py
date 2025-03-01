from config import SNAKE_BLINK_RANGE, SNAKE_BLINK_DURATION
from game_utils.direction import Direction
from sprites.snake_sprite import SnakeSprite
from sprites.sprite_utils import get_sprite_dir, get_sprite_wiggle
from utils import get_random_time, get_time_ms


class SnakeDrawer:
    def __init__(self, gui, snake_logic):
        self.gui = gui
        self.logic = snake_logic
        self.sprites = SnakeSprite()
        self.last_blink = get_time_ms()
        self.blink_wait = get_random_time(SNAKE_BLINK_RANGE)
        self.is_blinking = True

    def draw(self, screen):
        last_index = len(self.logic.body) - 1
        for i, segment in enumerate(self.logic.body):
            wiggle = (self.logic.wiggle_offset + i) % 2

            if i == 0:
                spr = get_sprite_wiggle(wiggle, self.sprites.head)
                spr = get_sprite_dir(self.logic.direction, spr)
                if self.check_blink():
                    eyelids = get_sprite_wiggle(wiggle, self.sprites.eyelids)
                    eyelids = get_sprite_dir(self.logic.direction, eyelids)
                    spr = self.gui.overlay_sprite(spr, eyelids)
            else:
                if i == last_index:
                    direction = calc_direction(self.logic.body[i - 1], segment)
                    spr = get_sprite_wiggle(wiggle, self.sprites.tail)
                    spr = get_sprite_dir(direction, spr)
                else:
                    first_dir = calc_direction(self.logic.body[i - 1], segment)
                    second_dir = calc_direction(segment, self.logic.body[i + 1])

                    if first_dir == second_dir:
                        spr = get_sprite_wiggle(wiggle, self.sprites.body)
                        spr = get_sprite_dir(first_dir, spr)
                    else:
                        direction = calc_curve_dir(first_dir, second_dir)
                        spr = get_sprite_dir(direction, self.sprites.curve)

            self.gui.draw_sprite(screen, spr, segment[0], segment[1])

    def check_blink(self):
        if get_time_ms() - self.last_blink >= self.blink_wait:
            self.blink_wait = get_random_time(SNAKE_BLINK_RANGE)
            self.last_blink = get_time_ms()
            return True

        return get_time_ms() - self.last_blink <= SNAKE_BLINK_DURATION


def calc_direction(prev, curr):
    delta = curr[0] - prev[0]
    if delta > 0:
        return Direction.left
    elif delta < 0:
        return Direction.right
    else:
        delta = curr[1] - prev[1]
        if delta > 0:
            return Direction.up
        elif delta < 0:
            return Direction.down
        else:
            print("Error, Snake positions overlap")


def calc_curve_dir(first_dir, second_dir):
    if (
        first_dir == Direction.up
        and second_dir == Direction.right
        or first_dir == Direction.left
        and second_dir == Direction.down
    ):
        return Direction.up
    elif (
        first_dir == Direction.down
        and second_dir == Direction.right
        or first_dir == Direction.left
        and second_dir == Direction.up
    ):
        return Direction.left
    elif (
        first_dir == Direction.down
        and second_dir == Direction.left
        or first_dir == Direction.right
        and second_dir == Direction.up
    ):
        return Direction.down
    elif (
        first_dir == Direction.up
        and second_dir == Direction.left
        or first_dir == Direction.right
        and second_dir == Direction.down
    ):
        return Direction.right

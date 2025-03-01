from game_utils.direction import Direction
from sprites.snake_sprite import SnakeSprite
from sprites.sprite_utils import get_sprite_dir, get_sprite_wiggle
from utils import get_random_time, get_time_ms

# time is in milliseconds
BLINK_RANGE = (2000, 3600)  # start and end of time intervall where snake blinks once
BLINK_DURATION = 100  # duration of blink in milliseconds
DIZZY_RANGE = (200, 400)  # pause between individual blinks while disoriented
DIZZY_DURATION = 2000  # duration where the snake blinks wildly before it's k.o.


class SnakeDrawer:
    def __init__(self, gui, snake_logic):
        self.gui = gui
        self.logic = snake_logic
        self.sprites = SnakeSprite()
        self.last_blink = get_time_ms()
        self.blink_wait = get_random_time(BLINK_RANGE)
        self.dizzy_blink_start = None

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
                if not self.logic.is_hurt:
                    spr = get_sprite_wiggle(wiggle, self.sprites.head)
                    spr = get_sprite_dir(self.logic.direction, spr)
                    if self.check_normal_blink():
                        eyelids = get_sprite_wiggle(wiggle, self.sprites.eyelids)
                        eyelids = get_sprite_dir(self.logic.direction, eyelids)
                        spr = self.gui.overlay_sprite(spr, eyelids)
                else:
                    spr = get_sprite_dir(
                        self.logic.direction, self.sprites.head_smushed
                    )
                    if self.check_dizzy_blink():
                        eyelids = get_sprite_dir(
                            self.logic.direction, self.sprites.eyelids_smushed
                        )
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

    def check_blink(self, range_):
        if get_time_ms() - self.last_blink >= self.blink_wait:
            self.blink_wait = get_random_time(range_)
            self.last_blink = get_time_ms()
            return True

        return get_time_ms() - self.last_blink <= BLINK_DURATION

    def check_normal_blink(self):
        return self.check_blink(BLINK_RANGE)

    def check_dizzy_blink(self):
        #  reset and setup for desoriented blinking
        if self.dizzy_blink_start is None:
            self.dizzy_blink_start = get_time_ms()
            self.last_blink = get_time_ms()
            self.blink_wait = get_random_time(DIZZY_RANGE)
        elif get_time_ms() - self.dizzy_blink_start >= DIZZY_DURATION:
            return True

        return self.check_blink(DIZZY_RANGE)

    def set_logic(self, logic):
        self.logic = logic
        self.dizzy_blink_start = None


def calc_direction(prev, curr):
    delta = curr[0] - prev[0]
    if delta > 0:
        return Direction.WEST
    elif delta < 0:
        return Direction.EAST
    else:
        delta = curr[1] - prev[1]
        if delta > 0:
            return Direction.NORTH
        elif delta < 0:
            return Direction.SOUTH
        else:
            print("Error, Snake positions overlap")


def calc_curve_dir(first_dir, second_dir):
    if (
        first_dir == Direction.NORTH
        and second_dir == Direction.EAST
        or first_dir == Direction.WEST
        and second_dir == Direction.SOUTH
    ):
        return Direction.NORTH
    elif (
        first_dir == Direction.SOUTH
        and second_dir == Direction.EAST
        or first_dir == Direction.WEST
        and second_dir == Direction.NORTH
    ):
        return Direction.WEST
    elif (
        first_dir == Direction.SOUTH
        and second_dir == Direction.WEST
        or first_dir == Direction.EAST
        and second_dir == Direction.NORTH
    ):
        return Direction.SOUTH
    elif (
        first_dir == Direction.NORTH
        and second_dir == Direction.WEST
        or first_dir == Direction.EAST
        and second_dir == Direction.SOUTH
    ):
        return Direction.EAST

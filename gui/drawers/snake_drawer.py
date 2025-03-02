from game_utils.direction import Direction, Collision
from sprites.snake_sprite import SnakeSprite
from sprites.sprite_utils import get_sprite_dir, get_sprite_wiggle, WIGGLE_L, WIGGLE_R
from utils import get_random_time, get_time_ms

# time is in milliseconds
BLINK_RANGE = (2000, 3600)  # start and end of time intervall where snake blinks once
BLINK_DURATION = 100  # duration of blink in milliseconds
DIZZY_OFFSET = 250  # when the dizzy animation starts after colliding
DIZZY_SPEED = 100  # time each frame of animation is shown


class SnakeDrawer:
    def __init__(self, gui, snake_logic):
        self.gui = gui
        self.logic = snake_logic
        self.sprites = SnakeSprite()
        self.last_blink = get_time_ms()
        self.blink_wait = get_random_time(BLINK_RANGE)
        self.collision_time = None
        self.dizzy_index = 0
        self.last_dizzy_change = None

    def draw(self, screen):
        last_index = len(self.logic.body) - 1
        for i in range(len(self.logic.body) - 1, -1, -1):
            segment = self.logic.body[i]
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

                spr = self.animate_head(wiggle)
            elif i == last_index:
                spr = self.animate_tail(i, segment, wiggle)
            else:
                spr = self.animate_body(i, segment, wiggle)

            self.gui.draw_sprite(screen, spr, segment[0], segment[1])

    def animate_head(self, wiggle):
        if self.logic.collided_with is None:
            spr = get_sprite_dir(self.logic.direction, self.sprites.head)
            if self.check_normal_blink():
                eyelids = get_sprite_dir(self.logic.direction, self.sprites.eyelids)
                spr = self.gui.overlay_sprite(spr, eyelids)
        else:
            if self.collision_time is None:
                self.collision_time = get_time_ms()
                self.last_dizzy_change = self.collision_time + DIZZY_OFFSET
            spr = self.animate_collision()

        return spr

    def animate_collision(self):
        if get_time_ms() - self.collision_time <= DIZZY_OFFSET:
            if self.logic.collided_with.val() == self.logic.prev_direction.val():
                return get_sprite_dir(self.logic.direction, self.sprites.hit_wall)

            match self.logic.collided_with:
                case Collision.BODY:
                    return get_sprite_dir(self.logic.direction, self.sprites.hit_body)
                case Collision.CURVE:
                    return self.get_hit_curve_sprite()
                case Collision.TAIL:
                    return self.get_hit_tail_spr()
                case Collision.LEFT:
                    return self.animate_side_collision(Direction.NORTH, Direction.SOUTH)
                case Collision.TOP:
                    return self.animate_side_collision(Direction.EAST, Direction.WEST)
                case Collision.RIGHT:
                    return self.animate_side_collision(Direction.SOUTH, Direction.NORTH)
                case Collision.TOP:
                    return self.animate_side_collision(Direction.WEST, Direction.EAST)
                case _:
                    print("Collison collided_with has unexpected value")
        else:
            spr = get_sprite_dir(self.logic.prev_direction, self.sprites.head)
            direction = self.logic.prev_direction
            if self.logic.collided_with == Collision.BODY:
                direction = self.logic.direction
                spr = get_sprite_dir(direction, self.sprites.hit_body)
            elif self.logic.collided_with == Collision.CURVE:
                direction = self.logic.direction
                spr = self.get_hit_curve_sprite()
            elif self.logic.collided_with == Collision.TAIL:
                direction = self.logic.direction
                spr = self.get_hit_tail_spr()

            dizzy_eyes = get_sprite_dir(direction, self.sprites.dizzy_eyes)
            if get_time_ms() - self.last_dizzy_change >= DIZZY_SPEED:
                self.dizzy_index += 1
                if self.dizzy_index == len(dizzy_eyes):
                    self.dizzy_index = 0

            return self.gui.overlay_sprite(spr, dizzy_eyes[self.dizzy_index])

    def animate_side_collision(self, dir_1, dir_2):
        spr = self.sprites.hit_side
        if self.logic.prev_direction == dir_1:
            spr = get_sprite_wiggle(WIGGLE_L, spr)
        elif self.logic.prev_direction == dir_2:
            spr = get_sprite_wiggle(WIGGLE_R, spr)
        else:
            print(
                f"Wrong Direction while hitting wall. dir: {self.logic.prev_direction.val()}, coll: {self.logic.collided_with.val()}"
            )
        return get_sprite_dir(self.logic.prev_direction, spr)

    def animate_body(self, i, segment, wiggle):
        first_dir = calc_direction(self.logic.body[i - 1], segment)
        second_dir = calc_direction(segment, self.logic.body[i + 1])
        if first_dir == second_dir:
            spr = get_sprite_wiggle(wiggle, self.sprites.body)
            spr = get_sprite_dir(first_dir, spr)
        else:
            direction = calc_curve_dir(first_dir, second_dir)
            spr = get_sprite_dir(direction, self.sprites.curve)
        return spr

    def animate_tail(self, i, segment, wiggle):
        direction = calc_direction(self.logic.body[i - 1], segment)
        spr = get_sprite_wiggle(wiggle, self.sprites.tail)
        spr = get_sprite_dir(direction, spr)
        return spr

    def get_hit_tail_spr(self):
        wiggle = WIGGLE_L
        tail_dir = calc_direction(self.logic.body[-2], self.logic.body[0])
        if (
            (self.logic.direction == Direction.WEST and tail_dir == Direction.NORTH)
            or (self.logic.direction == Direction.NORTH and tail_dir == Direction.EAST)
            or (self.logic.direction == Direction.EAST and tail_dir == Direction.SOUTH)
            or (self.logic.direction == Direction.SOUTH and tail_dir == Direction.WEST)
        ):
            wiggle = WIGGLE_R
        spr = get_sprite_wiggle(wiggle, self.sprites.hit_tail)
        spr = get_sprite_dir(self.logic.direction, spr)
        return spr

    def get_hit_curve_sprite(self):
        wiggle = WIGGLE_L
        i = self.logic.body[1:].index(self.logic.body[0])
        first_dir = calc_direction(self.logic.body[i - 1], self.logic.body[i])
        second_dir = calc_direction(self.logic.body[i], self.logic.body[i + 1])
        curve_dir = calc_curve_dir(first_dir, second_dir)
        if (
            (self.logic.direction == Direction.WEST and curve_dir == Direction.NORTH)
            or (self.logic.direction == Direction.NORTH and curve_dir == Direction.EAST)
            or (self.logic.direction == Direction.EAST and curve_dir == Direction.SOUTH)
            or (self.logic.direction == Direction.SOUTH and curve_dir == Direction.WEST)
        ):
            wiggle = WIGGLE_R
        spr = get_sprite_wiggle(wiggle, self.sprites.hit_curve)
        spr = get_sprite_dir(self.logic.direction, spr)
        return spr

    def check_blink(self, range_):
        if get_time_ms() - self.last_blink >= self.blink_wait:
            self.blink_wait = get_random_time(range_)
            self.last_blink = get_time_ms()
            return True

        return get_time_ms() - self.last_blink <= BLINK_DURATION

    def check_normal_blink(self):
        return self.check_blink(BLINK_RANGE)

    def set_logic(self, logic):
        self.logic = logic
        self.collided_with = None
        self.collision_time = None
        self.dizzy_index = 0
        self.last_dizzy_change = None


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

import pygame

from defs import Collision, Direction
from gui.gui_utils import to_px, overlay_sprite
from gui.sprites.snake_sprite import SnakeSprite
from gui.sprites.sprite_utils import (
    get_sprite_dir,
    get_sprite_wiggle,
    WIGGLE_L,
    WIGGLE_R,
)
from utils import get_random_time, get_time_ms

# time is in milliseconds
BLINK_RANGE = (2000, 3600)  # start and end of time intervall where snake blinks once
BLINK_DURATION = 100  # duration of blink in milliseconds
DIZZY_OFFSET = 250  # when the dizzy animation starts after colliding
DIZZY_SPEED = 100  # time each frame of animation is shown


class SnakeDrawer:
    """
    Responsible for drawing the desired sprites of the snake.
    :param snake_logic: Reference to the corresponding :class:`SnakeLogic` instance.
    ::
    """

    def __init__(self, snake_logic):
        self.logic = snake_logic
        self.sprites = SnakeSprite()
        self.last_blink = get_time_ms()
        self.blink_wait = get_random_time(BLINK_RANGE)
        self.collision_time = None
        self.dizzy_index = 0
        self.last_dizzy_change = None
        self.has_eaten: int = 0

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws sprites to the :attr:`screen`.
        :return: Noting.
        """
        last_index = len(self.logic.body) - 1
        for i in range(len(self.logic.body) - 1, -1, -1):
            segment = self.logic.body[i]
            wiggle = (self.logic.wiggle_offset + i) % 2

            if i == 0:
                spr = self.animate_head()
            elif i == last_index:
                spr = self.animate_tail(i, segment, wiggle)
            else:
                spr = self.animate_body(i, segment, wiggle)

            pos = (to_px(segment[0]), to_px(segment[1]))
            screen.blit(spr, pos)

    def animate_head(self) -> pygame.Surface:
        """
        Selecting the correct sprite or animation for the head.
        :return: The selected sprite.
        ::
        """
        if self.logic.collided_with is None:
            spr = get_sprite_dir(self.logic.direction, self.eating_animation())
            if self.check_blink():
                eyelids = get_sprite_dir(self.logic.direction, self.sprites.eyelids)
                spr = overlay_sprite(spr, eyelids)
        else:
            if self.collision_time is None:
                self.collision_time = get_time_ms()
                self.last_dizzy_change = self.collision_time + DIZZY_OFFSET
            spr = self.collision_animation()

        return spr

    def eating_animation(self) -> pygame.Surface:
        """
        Selecting the correct sprite of the head for the eating animation.
        :return: The selected sprite.
        ::
        """
        if self.logic.is_food_ahead():
            self.has_eaten = 3
            return self.sprites.mouth
        elif self.has_eaten > 0:
            self.has_eaten -= 1
            if self.has_eaten == 2:
                return self.sprites.head
            else:
                return self.sprites.tongue
        else:
            return self.sprites.head

    def collision_animation(self) -> pygame.Surface:
        """
        Selecting the correct sprite of the head for the colliding animation.
        :return: The selected sprite.
        ::
        """
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
                    return self.side_collision_animation(
                        Direction.NORTH, Direction.SOUTH
                    )
                case Collision.TOP:
                    return self.side_collision_animation(Direction.EAST, Direction.WEST)
                case Collision.RIGHT:
                    return self.side_collision_animation(
                        Direction.SOUTH, Direction.NORTH
                    )
                case Collision.TOP:
                    return self.side_collision_animation(Direction.WEST, Direction.EAST)
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

            return overlay_sprite(spr, dizzy_eyes[self.dizzy_index])

    def side_collision_animation(
        self, dir_1: Direction, dir_2: Direction
    ) -> pygame.Surface:
        """
        Selecting the correct sprite of the head for the side colliding animation.
        :param dir_1: The first direction the snake could have been travelling before hitting the wall.
        :param dir_2: The second direction the snake could have been travelling before hitting the wall.
        :return: The selected sprite.
        ::
        """
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

    def animate_body(
        self, i: int, segment: tuple[int, int], wiggle: int
    ) -> pygame.Surface:
        """
        Selecting the correct sprite for the body.
        :param i: Index of the current segment in :attr:`self.logic.body`.
        :param segment: Position of the current segment.
        :type segment: x, y
        :param wiggle: The wiggle-direction for the current segment.
        :return: The selected sprite.
        ::
        """
        first_dir = calc_direction(self.logic.body[i - 1], segment)
        second_dir = calc_direction(segment, self.logic.body[i + 1])
        if first_dir == second_dir:
            spr = get_sprite_wiggle(wiggle, self.sprites.body)
            spr = get_sprite_dir(first_dir, spr)
        else:
            direction = calc_curve_dir(first_dir, second_dir)
            spr = get_sprite_dir(direction, self.sprites.curve)
        return spr

    def animate_tail(
        self, i: int, segment: tuple[int, int], wiggle: int
    ) -> pygame.Surface:
        """
        Selecting the correct sprite for the tail.
        :param i: Index of the tail in :attr:`self.logic.body`.
        :param segment: Position of the tail.
        :type segment: x, y
        :param wiggle: The wiggle-direction for the tail.
        :return: The selected sprite.
        ::
        """
        direction = calc_direction(self.logic.body[i - 1], segment)
        spr = get_sprite_wiggle(wiggle, self.sprites.tail)
        spr = get_sprite_dir(direction, spr)
        return spr

    def get_hit_tail_spr(self) -> pygame.Surface:
        """
        Getting the correct sprite for the head hitting the tail.
        :return: The selected sprite.
        ::
        """
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

    def get_hit_curve_sprite(self) -> pygame.Surface:
        """
        Getting the correct sprite for the head hitting a curve of the body.
        :return: The selected sprite.
        ::
        """
        wiggle = WIGGLE_L
        i = self.logic.body[1:].index(self.logic.body[0]) + 1
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

    def check_blink(self) -> bool:
        """
        Checks if snake needs to blink
        and also resets timer and the random interval :attr:`self.blink_wait`.
        :return: Whehter to blink or not.
        ::
        """
        if get_time_ms() - self.last_blink >= self.blink_wait:
            self.blink_wait = get_random_time(BLINK_RANGE)
            self.last_blink = get_time_ms()
            return True

        return get_time_ms() - self.last_blink <= BLINK_DURATION

    def set_logic(self, logic) -> None:
        """
        Sets a new :class:`SnakeLogic` reference and resets some other stuff.
        :param logic: Reference of a :class:`SnakeLogic` instance.
        :return: Nothing.
        """
        self.logic = logic
        self.collided_with = None
        self.collision_time = None
        self.dizzy_index = 0
        self.last_dizzy_change = None


def calc_direction(prev: tuple[int, int], curr: tuple[int, int]) -> Direction:
    """
    A function for calculating a :class:`Direction` between :attr:`prev` and :attr:`curr`.
    Forgot what exactly the resulting :class:`Direction` means, and I'm too lazy to find out.
    It works so it's ok, probably don't touch again.
    :param prev: The previous position.
    :type prev: x, y
    :param curr: The current position.
    :type curr: x, y
    :return: The calculated :class:`Direction`
    ::
    """
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


def calc_curve_dir(first_dir: Direction, second_dir: Direction) -> Direction:
    """
    Calculates the :class:`Direction` (= orientation) of the curve-sprite.
    :param first_dir: First direction.
    :param second_dir: Second direction.
    :return: Calculated orientation.
    """
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

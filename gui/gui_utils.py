import pygame

import config


def to_px(coord: int) -> int:
    """
    Calculates pixel value for given coord.
    """
    return coord * config.SPRITE_SIZE


def overlay_sprite(base: pygame.Surface, top: pygame.Surface):
    """
    Draws :attr:`top` ontop of a copy of :attr:`base`.
    :return: New merged surface.
    ::
    **Notes**:
        Does not change any of the passed :class:`pygame.Surface`s.
    ::
    """
    base = base.copy()
    base.blit(top, (0, 0))
    return base

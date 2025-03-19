import os
from typing import Union

import pygame

import config
from defs import Direction


WIGGLE_L = 0
WIGGLE_R = 1


class SpriteVariant:
    """
    Holds every orienation of a sprite.
    :param input_sprite: The sprite in north-orientation.
    ::
    """

    def __init__(self, input_sprite: pygame.Surface):
        self.north = pygame.Surface.copy(input_sprite)
        self.west = pygame.transform.rotate(self.north, 90)
        self.south = pygame.transform.rotate(self.west, 90)
        self.east = pygame.transform.rotate(self.south, 90)


class Sprite:
    """
    Holds the default and mirrored version of a :class:`SpriteVariant`.
    :param input_sprite: The default sprite in north-orientation.
    ::
    """

    def __init__(self, input_sprite: pygame.Surface):
        sprite = pygame.Surface.copy(input_sprite)
        self.left = SpriteVariant(sprite)
        sprite = pygame.transform.flip(sprite, True, False)
        self.right = SpriteVariant(sprite)


class SpriteVariantList:
    """
    Holds a list of sprites for every orientation.
    :param input_sprite_list: A list of sprites in north-orientation.
    ::
    """

    def __init__(self, input_sprite_list: list[pygame.Surface]):
        self.north = []
        for sprite in input_sprite_list:
            self.north.append(sprite.copy())
        self.west = self.rotate_list(self.north)
        self.south = self.rotate_list(self.west)
        self.east = self.rotate_list(self.south)

    def rotate_list(self, input_list: list[pygame.Surface]) -> list[pygame.Surface]:
        """
        Rotates a list of sprites by 90 degrees counter-clockwise.
        :param input_list: The list of sprites to be rotated; will not be modified.
        :return: New list with rotated sprites.
        ::
        """
        out_list = []
        for sprite in input_list:
            rot_sprite = pygame.transform.rotate(sprite, 90)
            out_list.append(rot_sprite)
        return out_list


#############
# Functions #
#############


def load_sprite(name: str) -> pygame.Surface:
    """
    Loads a sprite,
    and also converts it to a format where pygame recognizes transparency of png's.
    :param name: String of the filename; just the name without a path or file-endings.
    :return: The loaded sprite.
    ::
    """
    img = pygame.image.load(create_sprite_path(name))
    sprite = img.convert_alpha()
    return sprite


def load_spritesheet(name: str) -> list[pygame.Surface]:
    """
    Loads a spritesheet of any dimension,
    and also converts it to a format where pygame recognizes transparency of png's.
    :param name: String of the filename; just the name without a path or file-endings.
    :return: A matrix of the individual sprites, arranged like on the spritsheet itself.
    ::
    """
    size = config.SPRITE_SIZE
    spritesheet = load_sprite(name)
    rows = int(spritesheet.get_height() / size)
    cols = int(spritesheet.get_width() / size)

    sprites = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # area of sprite in spritesheet
            sprite = spritesheet.subsurface(j * size, i * size, size, size)
            row.append(sprite)
        sprites.append(row)

    return sprites


def create_sprite_path(name: str) -> str:
    """
    Creates the relative path to the desired file in the sprite directory,
    with file ending.
    :param name: String of the filename; just the name without a path or file-endings.
    :return: The resulting path as a string.
    ::
    """
    return os.path.join(config.SPRITE_PATH, name + config.SPRITE_FILE_ENDING)


def get_sprite_dir(
    direction: Direction, sprite_variant: Union[SpriteVariant, SpriteVariantList]
) -> Union[pygame.Surface, list[pygame.Surface]]:
    """
    Gets the orientation of the sprite corresponding to the given direction.
    :param direction: The requested direction of the sprite.
    :sprite_variant: The sprite of which the correct orientation should be selected.
    :return: The requested orientation of the sprite
    ::
    **Notes**:
        Also works with list of Sprites (:class:`SpriteVariantList`)
    ::
    """
    if direction == Direction.WEST:
        return sprite_variant.west
    elif direction == Direction.SOUTH:
        return sprite_variant.south
    elif direction == Direction.EAST:
        return sprite_variant.east
    else:
        return sprite_variant.north


def get_sprite_wiggle(wiggle: int, sprite: Sprite) -> SpriteVariant:
    """
    Gets the default or mirrored version of the sprite according to the given wiggle.
    :param wiggle: The given wiggle (WIGGLE_L/WIGGLE_R).
    :param sprite: The sprite of which the version should be selected.
    :return: The choosen sprite version.
    ::
    """
    if wiggle == WIGGLE_R:
        return sprite.right
    else:
        return sprite.left

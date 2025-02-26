import os

import pygame

import config
from enums import Direction, Wiggle


class SpriteVariant:
    def __init__(self, input_sprite):
        self.north = pygame.Surface.copy(input_sprite)
        self.west = pygame.transform.rotate(self.north, 90)
        self.south = pygame.transform.rotate(self.west, 90)
        self.east = pygame.transform.rotate(self.south, 90)


class Sprite:
    def __init__(self, input_sprite):
        sprite = pygame.Surface.copy(input_sprite)
        self.left = SpriteVariant(sprite)
        sprite = pygame.transform.flip(sprite, False, True)
        self.right = SpriteVariant(sprite)


#############
# Functions #
#############


def load_sprite(name):
    img = pygame.image.load(create_sprite_path(name))
    sprite = img.convert_alpha()
    return sprite


def load_spritesheet(name):
    size = config.SPRITE_SIZE
    spritesheet = load_sprite(name)  # dict with spritename -> sprite surface
    rows = int(spritesheet.get_height() / size)
    cols = int(spritesheet.get_width() / size)
    print(f"{rows} {cols} {size}")

    sprites = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # area of sprite in spritesheet
            sprite = spritesheet.subsurface(j * size, i * size, size, size)
            row.append(sprite)
        sprites.append(row)

    return sprites


def create_sprite_path(name):
    return os.path.join(config.SPRITE_PATH, name + config.SPRITE_FILE_ENDING)


def get_sprite_dir(direction, sprite_variant):
    if direction == Direction.left:
        return sprite_variant.west
    elif direction == Direction.down:
        return sprite_variant.south
    elif direction == Direction.right:
        return sprite_variant.east
    else:
        return sprite_variant.north


def get_sprite_wiggle(wiggle, sprite):
    if wiggle == Wiggle.right:
        return sprite.right
    else:
        return sprite.left

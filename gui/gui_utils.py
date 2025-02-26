import os

import pygame

import config


def calc_x(x):
    return config.OFFSET_X + x * config.TILE_SIZE


def calc_y(y):
    return config.OFFSET_Y + y * config.TILE_SIZE


def draw_tile(screen, x, y, color):
    draw_rect(
        screen,
        calc_x(x),
        calc_y(y),
        config.TILE_SIZE,
        config.TILE_SIZE,
        color,
    )


def draw_rect(screen, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)


def draw_image(screen, image, x, y):
    screen.blit(image, (calc_x(x), calc_y(y)))


def load_sprite(name):
    img = pygame.image.load(create_sprite_path(name))
    sprite = pygame.Surface.convert(img)
    return sprite


def load_spritesheet(name, spritenames):
    size = config.SPRITE_SIZE
    count = len(spritenames)  # how many sprites should be extracted
    spritesheet = load_sprite(name)  # dict with spritename -> sprite surface
    rows = int(spritesheet.get_height / size)
    cols = int(spritesheet.get_width / size)

    sprites = {}
    for i in rows:
        for j in cols:
            index = i * cols + j
            if index >= count:
                return sprites
            # area of sprite in spritesheet
            selection_rect = pygame.Rect(i * size, j * size, size, size)
            sprite = spritesheet.subsurface(selection_rect)
            # add to output dict
            sprites[spritenames[i * cols + j]] = sprite

    return sprites


def create_sprite_path(name):
    return os.path.join(config.SPRITE_PATH, name + config.SPRITE_FILE_ENDING)

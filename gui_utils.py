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

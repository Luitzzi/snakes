import pygame
import config


# GUI
def calc_x(x):
    return config.OFFSET_X + x


def calc_y(y):
    return config.OFFSET_Y + y


def draw_tile(screen, x, y, color):
    draw_rect(
        screen,
        x * config.TILE_SIZE,
        y * config.TILE_SIZE,
        config.TILE_SIZE,
        config.TILE_SIZE,
        color,
    )


def draw_rect(screen, x, y, w, h, color):
    rect = pygame.Rect(calc_x(x), calc_y(y), w, h)
    pygame.draw.rect(screen, color, rect)

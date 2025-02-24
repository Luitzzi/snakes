import pygame
import config
import gui_utils


class SnakeSprite(pygame.sprite.Sprite):

    def __init__(self, snake_logic):
        super().__init__()
        self.snake_logic = snake_logic

    def draw(self, screen):
        for segment in self.snake_logic.body:
            gui_utils.draw_tile(screen, segment[0], segment[1], config.SNAKE_COLOR)

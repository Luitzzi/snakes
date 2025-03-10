import pygame
import config


class SnakeSprite(pygame.sprite.Sprite):

    def __init__(self, gui, snake_logic):
        super().__init__()
        self.gui = gui
        self.snake_logic = snake_logic

    def draw(self, screen):
        for segment in self.snake_logic.body:
            self.gui.draw_tile(screen, segment[0], segment[1], config.SNAKE_COLOR)

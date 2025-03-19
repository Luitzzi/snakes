import pygame

import config
from gui.gui_utils import calc_scaling_dim
from gui.views.game_view import GameView


class Gui:
    def __init__(self, game_logic):
        screen_res = config.SCREEN_RES
        self.screen = pygame.display.set_mode(screen_res)
        self.game_view = GameView(
            game_logic.field_size, game_logic.snake_logic, game_logic.food_logic
        )

        self.game_view_scaling_dim = calc_scaling_dim(
            self.game_view.field.get_size(), screen_res
        )

    def draw(self):
        view = self.game_view.capture(self.game_view_scaling_dim)

        self.screen.blit(view, (0, 0))

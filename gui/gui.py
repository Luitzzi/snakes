import pygame

import config
from gui.gui_utils import to_px
from gui.views.game_view import GameView


class Gui:
    """
    Handles everything gui related.
    :param game_logic: Reference to the :class:`Game` instance where :class:`Gui` is instanciated.
    ::
    """

    @staticmethod
    def calc_screen_res(
            field_size: tuple[int, int], padding: tuple[int, int, int, int], scale
    ) -> tuple[int, int]:
        """
        Calculates the resolution of the window from the given parameters.
        :param padding: Padding of the field from screen borders.
        :type padding: left, top, right, bottom
        :param field_size: Size of the field, in tiles not pixels.
        :type field_size: width, height
        :param scale: The scale the rendered image gets scaled by.
        :return: The calculated Resolution.
        ::
        """
        width = to_px(padding[0] + field_size[0] + padding[2]) * scale
        height = to_px(padding[1] + field_size[1] + padding[3]) * scale
        return width, height

    def __init__(self, game_logic):
        padding = (5, 2, 5, 2)
        scale = 3
        screen_res = Gui.calc_screen_res(game_logic.field_size, padding, scale)
        self.screen = pygame.display.set_mode(screen_res)
        self.game_view = GameView(
            screen_res,
            padding,
            game_logic.field_size,
            scale,
            game_logic.snake_logic,
            game_logic.food_logic,
        )
        self.game_logic = game_logic

    def draw(self) -> None:
        """
        Renders everything to the screen.
        :return: Nothing.
        ::
        """
        view = self.game_view.capture()
        self.screen.blit(view, (0, 0))
        pygame.display.flip()

    def game_restarted(self) -> None:
        """
        Hook to tell Gui when the game is restarted,
        so it can update the snake_logic reference of the snake_drawer.
        :return: Nothing.
        ::
        """
        self.game_view.field_view.snake_drawer.set_logic(self.game_logic.snake_logic)

    def __init_fonts(self):
        """
        Currently unneeded artefact of rebasing.
        """
        self.heading = pygame.font.Font(config.PIXEL_FONT_PATH, 32)
        self.subheading = pygame.font.Font(config.PIXEL_FONT_PATH, 20)
        self.text = pygame.font.Font(config.PIXEL_FONT_PATH, 15)

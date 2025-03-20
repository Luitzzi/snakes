import pygame

from gui.gui_utils import to_px
from gui.sprites.wall_sprite import WallSprite
from gui.views.field_view import FieldView


class GameView:
    """
    Responsible for rendering the whole game.
    :param screen_res: The resolution of the screen.
    :param padding: Padding of the field from screen borders.
    :type padding: left, top, right, bottom
    :param field_size: Size of the field, in tiles not pixels.
    :type field_size: width, height
    :param scale: The scale the rendered image gets scaled by.
    :param snake_logic: Reference to the corresponding :class:`SnakeLogic` instance.
    :param food_logic: Reference to the corresponding :class:`FoodLogic` instance.
    ::
    """

    field: pygame.Surface

    def __init__(
        self,
        screen_res: tuple[int, int],
        padding: tuple[int, int, int, int],
        field_size: tuple[int, int],
        scale: int,
        snake_logic,
        food_logic,
    ):
        self.scale = scale
        self.field_offset = (to_px(padding[0]), to_px(padding[1]))
        self.wall_sprite = WallSprite()
        self.field_view = FieldView(field_size, 1, snake_logic, food_logic)
        self.surf = self.__create_bg(screen_res, padding, field_size)

    def capture(self) -> pygame.Surface:
        """
        Renders the game and scales it by :attr:`self.scale`.
        :return: The rendered image.
        ::
        """
        surf = self.surf.copy()
        field = self.field_view.capture()
        surf.blit(field, self.field_offset)
        surf = pygame.transform.scale_by(surf, self.scale)
        return surf

    def __create_bg(
        self,
        res: tuple[int, int],
        padding: tuple[int, int, int, int],
        field_size: tuple[int, int],
    ) -> pygame.Surface:
        """
        Creates the background sprite for the game, including the walls around the field.
        :param res: The resolution of the screen.
        :param padding: Padding of the field from screen borders.
        :type padding: left, top, right, bottom
        :param field_size: Size of the field, in tiles not pixels.
        :type field_size: width, height
        :return: The resulting sprite.
        ::
        """
        # coordinates of the borders of the field
        left = to_px(padding[0] - 1)
        top = to_px(padding[1] - 1)
        right = to_px(padding[0] + field_size[0])
        bottom = to_px(padding[1] + field_size[1])

        # draw bg
        surf = pygame.Surface(res)
        for i in range(padding[1] + field_size[1] + padding[3]):
            for j in range(padding[0] + field_size[0] + padding[2]):
                pos = (to_px(j), to_px(i))
                surf.blit(self.wall_sprite.bg, pos)

        #   walls
        pos = (left, top)
        surf.blit(self.wall_sprite.top_left, pos)
        pos = (right, top)
        surf.blit(self.wall_sprite.top_right, pos)
        pos = (left, bottom)
        surf.blit(self.wall_sprite.bot_left, pos)
        pos = (right, bottom)
        surf.blit(self.wall_sprite.bot_right, pos)

        #   top and bottom wall
        for i in range(field_size[0]):
            x = left + to_px(i + 1)
            pos_top = (x, top)
            surf.blit(self.wall_sprite.top, pos_top)
            pos_bot = (x, bottom)
            surf.blit(self.wall_sprite.bot, pos_bot)

        #   left and right wall
        for i in range(field_size[1]):
            y = top + to_px(i + 1)
            pos_left = (left, y)
            surf.blit(self.wall_sprite.left, pos_left)
            pos_right = (right, y)
            surf.blit(self.wall_sprite.right, pos_right)

        return surf

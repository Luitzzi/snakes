import pygame

from gui.gui_utils import to_px
from gui.sprites.field_sprite import FieldSprite
from gui.drawers.food_drawer import FoodDrawer
from gui.drawers.snake_drawer import SnakeDrawer


class FieldView:
    """
    Responsible for rendering the field with the snake and food.
    :param field_size: Size of the field (in tiles not pixels).
    :type field_size: width, height
    :param scale: The scale the rendered image gets scaled by.
    :param snake_logic: Reference to the corresponding :class:`SnakeLogic` instance.
    :param food_logic: Reference to the corresponding :class:`FoodLogic` instance.
    ::
    """

    field: pygame.Surface

    def __init__(
        self, field_size: tuple[int, int], scale: int, snake_logic, food_logic
    ):
        self.scale = scale
        self.field_sprite = FieldSprite()
        self.food_drawer = FoodDrawer(food_logic)
        self.snake_drawer = SnakeDrawer(snake_logic)
        self.surf = self.__create_field(field_size)

    def capture(self) -> pygame.Surface:
        """
        Renders the field, food and snake and scales it by :attr:`self.scale`.
        :return: The rendered image.
        ::
        """
        surf = self.surf.copy()
        self.food_drawer.draw(surf)
        self.snake_drawer.draw(surf)
        surf = pygame.transform.scale_by(surf, self.scale)
        return surf

    def __create_field(self, size) -> pygame.Surface:
        """
        Creates the field (the alternating grass pattern) sprite.
        :param field_size: size of the field (in tiles not pixels).
        :type field_size: width, height
        :return: The resulting sprite.
        ::
        """
        field_res = (to_px(size[0]), to_px(size[1]))
        field = pygame.Surface(field_res)
        # draw grass
        for i in range(size[0]):
            for j in range(size[1]):
                if (i + j) % 2 == 0:
                    spr = self.field_sprite.dark
                else:
                    spr = self.field_sprite.light
                pos = (to_px(j), to_px(i))
                field.blit(spr, pos)
        return field

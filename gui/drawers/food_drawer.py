from gui.sprites.food_sprite import FoodSprite

from gui.gui_utils import to_px


class FoodDrawer:
    """
    Responsible for drawing the desired sprite of the food.
    :param food_logic: Reference to the corresponding :class:`FoodLogic` instance.
    ::
    """

    def __init__(self, food_logic):
        self.food_logic = food_logic
        self.sprites = FoodSprite()

    def draw(self, screen) -> None:
        """
        Draws sprite to the :attr:`screen`.
        :return: Noting.
        """
        location = self.food_logic.location
        pos = (
            to_px(location[0]),
            to_px(location[1]),
        )
        screen.blit(self.sprites.apple_red, pos)

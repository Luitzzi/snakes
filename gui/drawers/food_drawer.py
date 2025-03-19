from gui.sprites.food_sprite import FoodSprite

from gui.gui_utils import coord_to_px


class FoodDrawer:
    def __init__(self, food_logic):
        self.food_logic = food_logic
        self.sprites = FoodSprite()

    def draw(self, screen):
        location = self.food_logic.location
        pos = (
            coord_to_px(location[0] + 1),
            coord_to_px(location[1] + 1),
        )
        screen.blit(self.sprites.apple_red, pos)

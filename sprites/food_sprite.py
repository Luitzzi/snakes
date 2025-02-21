import pygame.sprite
import config
import gui_utils


class FoodSprite(pygame.sprite.Sprite):

    def __init__(self, food_logic):
        super().__init__()
        self.food_logic = food_logic
        self.raw_image = pygame.image.load("assets/apple.png")
        self.image = pygame.transform.scale(
            self.raw_image, (config.TILE_SIZE, config.TILE_SIZE)
        )

    def draw(self, screen):
        gui_utils.draw_image(
            screen, self.image, self.food_logic.location[0], self.food_logic.location[1]
        )

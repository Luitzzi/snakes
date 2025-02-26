import pygame.sprite
import config


class FoodSprite(pygame.sprite.Sprite):
    def __init__(self, gui, food_logic):
        super().__init__()
        self.gui = gui
        self.food_logic = food_logic
        self.raw_image = pygame.image.load(config.TOMATO_IMAGE_PATH)
        self.image = self.gui.transform_image(self.raw_image)

    def draw(self, screen):
        self.gui.draw_image(
            screen, self.image, self.food_logic.location[0], self.food_logic.location[1]
        )

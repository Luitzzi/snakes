import random
import config
import utils


class Food:
    def __init__(self):
        self.location = None
        self.respawn()

    def draw(self, screen):
        utils.draw_tile(screen, self.location[0], self.location[1], config.FOOD_COLOR)

    def respawn(self):
        self.location = (
            random.randrange(0, config.WIDTH),
            random.randrange(0, config.HEIGHT),
        )

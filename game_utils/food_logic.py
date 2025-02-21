import random
import config
import gui_utils


class FoodLogic:
    def __init__(self):
        self.location = None
        self.respawn(config.SNAKE_STARTING_POSITION)

    def respawn(self, snake_body):
        valid_location = False
        while not valid_location:
            new_location = (
                random.randrange(0, config.WIDTH),
                random.randrange(0, config.HEIGHT),
            )
            valid_location = self.__is_location_valid(new_location, snake_body)
        self.location = new_location

    def __is_location_valid(self, new_location, snake_body):
        if new_location in snake_body:
            return False
        else:
            return True

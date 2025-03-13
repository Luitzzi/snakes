import random
import config
import gui_utils


class FoodLogic:
    def __init__(self, snake_starting_position, field_width, field_height):
        self.field_width = field_width
        self.field_height = field_height
        self.location = None
        self.respawn(snake_starting_position)

    def respawn(self, snake_body):
        valid_location = False
        while not valid_location:
            new_location = (
                random.randrange(0, config.WIDTH),
                random.randrange(0, config.HEIGHT),
            )
            valid_location = self.__is_location_valid(new_location, snake_body)
        self.location = new_location

    def set_food_position(self, position):
        self.location = position

    def __is_location_valid(self, new_location, snake_body):
        if new_location in snake_body:
            return False
        else:
            return True

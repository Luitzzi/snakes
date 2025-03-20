import random


class FoodLogic:
    def __init__(self, field_size: tuple[int, int]):
        self.field_width = field_size[0]
        self.field_height = field_size[1]
        self.location = None
        self.respawn()

    def respawn(self, snake_body=[(-1,-1)]):
        #TODO: Implement that the food can't spawn in the body of the snake
        valid_location = False
        while not valid_location:
            new_location = (
                random.randrange(0, self.field_width),
                random.randrange(0, self.field_height),
            )
            valid_location = self.__is_location_valid(new_location, snake_body)
        self.location = new_location

    def set_food_position(self, position):
        self.location = position

    @staticmethod
    def __is_location_valid(new_location, snake_body):
        if new_location in snake_body:
            return False
        else:
            return True

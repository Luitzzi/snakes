import numpy as np

class GameStatistics:
    default_capacity_food_positions = 200
    default_capacity_step_data = 10000

    def __init__(self, starting_position):
        self.score = 0
        self.time_alive = 0
        self.starting_position = starting_position
        self.food_positions = np.empty(self.default_capacity_food_positions, dtype=np.int16)
        self.num_food_positions = 0 # One food_position = Two food_positions elements x and y
        self.step_data = np.empty(self.default_capacity_step_data, dtype=np.int8)
        self.num_steps = 0

    def add_step(self, new_direction, new_food_position = None):
        """
        Compress the user-input in the form of the resulting change in direction in one byte step_data.
        Furthermore, add the new_food_position to the food_positions array if the snake ate.
        To be able to replay the game later the bool snake_ate is saved into the step_data byte.

        Formation of the step_data byte:
        0 0 0 0 0 0 0 0
                      ^ snake_ate: bool
                  ^ ^   new_direction: 00 north, 01 east, 10 south, 11 west

        :param new_direction: New direction resulting from the user input. 0 = north, 1 = east, 2 = south, 3 = west.
        :param new_food_position: The new_food_position as a tuple (x,y). Necessary if snake_ate = True.
        """
        bitcode_step_data = new_direction << 1
        if new_food_position:
            self.food_positions[self.num_food_positions * 2] = new_food_position[0]
            self.food_positions[self.num_food_positions * 2 + 1] = new_food_position[1]
            bitcode_step_data |= 1
            self.num_food_positions += 1

        self.step_data[self.num_steps] = bitcode_step_data
        self.num_steps += 1

    def add_terminating_step(self, score, time_alive, new_direction):
        self.score = score,
        self.time_alive = time_alive
        self.add_step(new_direction)


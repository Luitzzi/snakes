from typing import override

import numpy as np

from game.game_objects.direction import Direction
from game.player.player import Player

class AIAgent(Player):
    color: None

    def __init__(self, color):
        self.color = color

    @override
    def play_step(self) -> Direction:

    @staticmethod
    def get_state(self):
        """
        Returns the current state of the environment as a numpy array
        with 11 values:
        [is_danger_left, is_danger_straight, is_danger_right
         north, east, south, west, <- current direction
         north, east, south, west] <- food direction
        :return: numpy array of bools represented by 0 and 1 with 11 values
        """
        danger_positions = self.__get_danger_positions()
        current_direction = self.__get_current_direction()
        food_direction = self.__get_direction_of_food()

        state = danger_positions + current_direction + food_direction
        return np.array(state, dtype=int)

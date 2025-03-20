import unittest
import numpy as np
from db.game_statistics import GameStatistics

class TestReplay(unittest.TestCase):

    def setUp(self):
        self.game_stats = GameStatistics((5,5))

    def test_add_step(self):
        # Test case: snake_ate = False
        for direction in range(4):
            self.game_stats.add_step(direction)

        np.testing.assert_array_equal(self.game_stats.step_data[:self.game_stats.num_steps],
                                      [0, 2, 4, 6],
                                      "Error add_step with snake_ate = True")

        # Test case: snake_ate = True
        food_positions = [(1,1), (2,2), (3,3), (4,4)]
        for direction in range(4):
            self.game_stats.add_step(direction, food_positions[direction])

        np.testing.assert_array_equal(self.game_stats.step_data[4:self.game_stats.num_steps],
                                      [1, 3, 5, 7],
                                      "Error add_step with snake_ate = True")
        np.testing.assert_array_equal(self.game_stats.food_positions[:self.game_stats.num_food_positions * 2],
                                      [1, 1, 2, 2, 3, 3, 4, 4],
                                      "Error food_positions")


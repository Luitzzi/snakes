from typing import override

import pygame

import config
from game.game_objects.direction import Direction
from game.game_objects.snake_logic import SnakeLogic
from game.game_objects.food_logic import FoodLogic
from game.game_state import GameState
from game.playable.playable import Playable

class Singleplayer(Playable):

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time_alive = None
        self.score = None

        self.snake_starting_position = config.calc_starting_position(self.gui.field_width, self.gui.field_height)
        self.snake_logic = SnakeLogic(self.snake_starting_position)
        self.snake_sprite = SnakeSprite(self.gui, self.snake_logic)
        self.food_logic = FoodLogic(self.snake_starting_position, self.gui.field_width, self.gui.field_height)
        self.food_sprite = FoodSprite(self.gui, self.food_logic)

    @override
    def play_step(self) -> GameState:
        """
        Update the game-state:
        - Make the move based on the direction saved in snake_logic
        - Check if the move results in a collision
        - Check if snake eats
        """
        self.snake_logic.move()

        if self._is_collision():
            self.time_alive = self.get_time_alive()
            return GameState.GAME_OVER

        self._handle_eating()
        return GameState.PLAYING

    def _is_collision(self):
        """
        Check if the new_head results in a collision.
        The parameter is necessary to get the danger-moves in the training of the AI.
        :return: bool: True if collision occurred, False if not
        """
        new_head = self.snake_logic.get_head()
        if (
                new_head in self.snake_logic.body[1:]
                or new_head[0] < 0
                or new_head[0] >= self.gui.field_width
                or new_head[1] < 0
                or new_head[1] >= self.gui.field_height
        ):
            return True
        else:
            return False

    def _handle_eating(self):
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.food_logic.respawn(self.snake_logic.body)
            self.score += 1
        else:
            self.snake_logic.body.pop()

    def get_time_alive(self):
        """
        Returns how long the player is playing in the game_active state
        :return: int representing the time in seconds
        """
        if self.time_alive is None:
            return None
        else:
            running_time_millis = pygame.time.get_ticks() - self.time_alive
            return running_time_millis // 1000
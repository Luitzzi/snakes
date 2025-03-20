from abc import ABC, abstractmethod

from game.game_objects.direction import Direction

class Player(ABC):

    @abstractmethod
    def get_action(self) -> Direction:
        """
        Get the action the player performs at the current state of the game
        :return: Chosen action in the form of the new direction the snake should move.
        """
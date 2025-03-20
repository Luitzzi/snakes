from typing import List
from abc import ABC, abstractmethod

from game.game_state import GameState


class Playable(ABC):

    @abstractmethod
    def create_game(self, players: List[Player]) -> None:
        """
        Create a game with predefined players, for example Human, AIAgent etc.
        :param players:
        """

    @abstractmethod
    def play_step(self) -> GameState:
        """
        Execute on play_step and update the game logic
        """

from typing import override

from game.game_objects.direction import Direction
from game.player.player import Player

class AIAgent(Player):
    color: None

    def __init__(self, color):
        self.color = color

    @override
    def play_step(self) -> Direction:

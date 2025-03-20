from typing import override

import config
from event_handling.event_types import EventType
from game.game_objects.direction import Direction
from game.player.player import Player


class Human(Player):
    color: None
    current_direction: Direction

    def __init__(self, color):
        self.color = color
        self.current_direction = config.SNAKE_DEFAULT_DIRECTION

    @override
    def get_action(self) -> Direction:
        pass # Handled by the event_manager

    def player_input_handler(self, event_type):
        match event_type:
            case EventType.INPUT_EVENT.UP:
                if self.current_direction != Direction.SOUTH:
                    self.current_direction = Direction.NORTH
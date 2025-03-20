from typing import override

import config
from event_handling.event_types import EventType
from game.game_objects.direction import Direction
from game.game_objects.snake_logic import SnakeLogic
from game.player.player import Player


class Human(Player):
    color: None
    snake_logic: SnakeLogic

    def __init__(self, color, snake_logic: SnakeLogic):
        self.color = color
        self.snake_logic = snake_logic
        self.is_alive = True

    @override
    def get_action(self) -> Direction:
        """
        The action of a Human is determined by the key input of the player.
        Therefore, the method player_input_handler, called before game_manager.play_step()
        already gets the action.
        :return: Nothing because the direction already got updated
        """
        pass

    @override
    def execute_action(self, action=None) -> None:
        if self.is_alive:
            self.snake_logic.move()

    def player_input_handler(self, event_type: EventType) -> None:
        """
        Observer method registered at the event_handler for the event: INPUT_EVENT.
        Once any INPUT_EVENT such as w,a,s,d or the arrow-keys are pressed
        and the game_manager.game_state = PLAYING the method is triggered.
        :param event_type: INPUT_EVENT - w,a,s,d, arrow-keys
        :return:
        """
        match event_type:
            case EventType.INPUT_EVENT.UP:
                if self.snake_logic.direction != Direction.SOUTH:
                    self.snake_logic.direction = Direction.NORTH
            case EventType.INPUT_EVENT.RIGHT:
                if self.snake_logic.direction != Direction.WEST:
                    self.snake_logic.direction = Direction.EAST
            case EventType.INPUT_EVENT.DOWN:
                if self.snake_logic.direction != Direction.NORTH:
                    self.snake_logic.direction = Direction.SOUTH
            case EventType.INPUT_EVENT.LEFT:
                if self.snake_logic.direction != Direction.EAST:
                    self.snake_logic.direction = Direction.WEST
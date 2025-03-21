from event_handling.event_manager import EventManager
from event_handling.event_types import MovementEvent
from game.game_objects.snake_logic import SnakeLogic
from game.player.player import Player
from game.player.human_player import HumanPlayer
from game.player.player_type import PlayerType

class PlayerFactory:
    """
    Create Players dynamically at runtime using the factory pattern.
    """

    @staticmethod
    def create_player(player_type: PlayerType, color: int,
                      starting_position: tuple[int, int],
                      event_manager: EventManager) -> Player:
        """
        Creates a Player of a certain type, initialises and returns it.
        :param player_type: Specific type of the Player
        :param color: Color of the snake
        :param starting_position: (x,y) position of the field at that the snake starts
        :param event_manager: Enables to register Players for events
        :return: Player-Instance with the specific Type
        """
        match player_type:
            case PlayerType.HUMAN_PLAYER:
                player = HumanPlayer(color, SnakeLogic(starting_position))
                event_manager.register(MovementEvent, player.player_input_handler)

            case PlayerType.AI_AGENT:
                pass
            case PlayerType.REPLAY_AGENT:
                pass
            case _:
                raise ValueError("Unknown player type")
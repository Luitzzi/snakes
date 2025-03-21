from game.game_objects.snake_logic import SnakeLogic
from game.player.player import Player
from game.player.humanplayer import HumanPlayer
from game.player.player_type import PlayerType

class PlayerFactory:
    """
    Create Players dynamically at runtime using the factory pattern.
    """

    @staticmethod
    def create_player(player_type: PlayerType, color: int, starting_position: tuple[int, int]) -> Player:
        match player_type:
            case PlayerType.HUMAN_PLAYER:
                return HumanPlayer(color, SnakeLogic(starting_position))
            case PlayerType.AI_AGENT:
                pass
            case PlayerType.REPLAY_AGENT:
                pass
            case _:
                raise ValueError("Unknown player type")
from typing import List

import pygame

import config
from event_handling.event_manager import EventManager
from event_handling.event_types import EventType
from game.game_state import GameState
from game.playable.playable import Playable
from game.playable.singleplayer import Singleplayer
from game.player.player import Player
from game.player.player_factory import PlayerFactory
from game.player.player_type import PlayerType


class GameManager:
    """
    Manages which game logic gets updated at a certain state.
    """
    game_state: GameState
    event_manager: EventManager

    game: Playable
    field_size: tuple[int, int]
    starting_position: tuple[int, int]

    @staticmethod
    def quit_game() -> None:
        """
        Observer method registered at the event_handler for the event: GAME_QUIT.
        Once the event occurs it is triggered.
        :return:
        ::
        """
        print("Closing game...")
        pygame.quit()
        exit()

    def __init__(self, event_manager):
        self.game_state = GameState.TITLE_SCREEN
        self.event_manager = event_manager
        self.event_manager.register(EventType.GAME_QUIT, self.quit_game())

        self.game = None
        self.field_size = (config.DEFAULT_FIELD_WIDTH, config.DEFAULT_FIELD_HEIGHT)
        self.starting_position = (self.field_size[0] // 4, self.field_size[1] // 2)

    def start_game(self, player: Player, enemies: List[Player] = None) -> None:
        """
        Create a game with a player and optional enemies
        and change the game_state to Running.
        :param player: The real player playing the Singleplayer game.
        :param enemies: Computer enemies playing against the player.
        :return:
        ::
        """
        if enemies is None:
            enemies = []
        self.game = Singleplayer(player, enemies, self.field_size)
        self.game_state = GameState.PLAYING


    def update(self) -> None:
        """
        Determine based on the current game_state which logic needs an update.
        There are static and dynamic program-elements.
        Static elements: title_screen or game_over_screen.
        -> Just updates the inputs that occurred and change the game_state accordingly.
        Dynamic elements: All playable objects.
        -> Execute the play_step() and perform on step/tick on the playable object.

        :return:
        ::
        """
        match self.game_state:
            case GameState.TITLE_SCREEN:
                self.handle_title_screen()
            case GameState.PLAYING:
                if self.game:
                    self.game_state = self.game.play_step()
                else:
                    raise AttributeError("Object attribute 'game' is not initialized.")
            case GameState.GAME_OVER:
                self.handle_game_over_screen()

    def handle_title_screen(self):
        """
        Change the game_stated based on the input that occurred.
        Possible choices:
        - Play Singleplayer
        - Stats
        :return:
        ::
        """
        # Currently: Just directly start a game until we implemented a title_screen
        real_player = PlayerFactory.create_player(PlayerType.HUMAN_PLAYER, 1, self.starting_position)
        self.start_game(real_player)

    def handle_game_over_screen(self):
        """
        Displays the death-screen with the score and time_alive of the last round.
        Possible choices:
        - Replay: Space
        - Menu:
        :return:
        """
        pass
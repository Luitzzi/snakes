from event_handling.event_manager import EventManager
from event_handling.event_types import EventType
from game.game_state import GameState

class GameManager:
    game_state: GameState
    game: Playable
    event_manager: EventManager

    def __init__(self, event_manager):
        self.game_state = GameState.TITLE_SCREEN
        self.game = None

        self.event_manager = event_manager

    def start_game(self):
        pass

    def quit_game(self):
        self.event_manager.dispatch(EventType.GAME_QUIT)

    def update(self) -> None:
        match self.game_state:
            case GameState.TITLE_SCREEN:
                self.handle_title_screen()
            case GameState.PLAYING:
                if self.game:
                    self.game.play_step()
                else:
                    raise AttributeError("Object attribute 'game' is not initialized.")
            case GameState.GAME_OVER:
                self.handle_game_over_screen()

    def handle_title_screen(self):
        pass

    def handle_game_over_screen(self):
        pass
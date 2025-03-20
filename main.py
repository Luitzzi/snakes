import pygame

from event_handling.event_manager import EventManager
from event_handling.event_types import EventType
from game.game_manager import GameManager
from gui.gui import Gui


def game_loop() -> None:
    pygame.init()
    event_manager = EventManager()
    game_manager = GameManager(event_manager)
    gui = Gui(game_manager)

    running = True
    while running:
        event_manager.get_events()
        game_manager.update()
        gui.draw() # Rename to render


if __name__ == "__main__":
    game_loop()

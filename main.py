import pygame

from event_handling.event_manager import EventManager
from event_handling.event_types import EventType

def game_loop() -> None:
    event_manager = EventManager()
    game_state_manager = GameStateManager(event_manager)
    gui = GUI()
    pygame.init()

    running = True
    while running:
        handle_events(event_manager)
        game_state_manager.update()
        gui.render()


def handle_events(event_manager: EventManager) -> None:
    # TODO: Implement event management as a dict
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            event_manager.dispatch(EventType.GAME_QUIT)

        if event.type == pygame.KEYDOWN:
            # Game running events
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                event_manager.dispatch(EventType.INPUT_EVENT.UP)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                event_manager.dispatch(EventType.INPUT_EVENT.RIGHT)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                event_manager.dispatch(EventType.INPUT_EVENT.DOWN)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                event_manager.dispatch(EventType.INPUT_EVENT.LEFT)

            # Title screen events
            elif event.key == pygame.K_SPACE:
                event_manager.dispatch(EventType.START_GAME)


if __name__ == '__main__':
    game_loop()
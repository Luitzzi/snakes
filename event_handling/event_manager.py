from typing import Dict, List, Callable

import pygame

from event_types import EventType
from event_handlers.event_handler import EventHandler

class EventManager:
    handlers: Dict[EventType, List[Callable]]

    def __init__(self):
        self.handlers = {}

    def register(self, event_type: EventType, handler: Callable[[],None]) -> None:
        """
        Subscribe a handler to a certain event_type.
        This links the event_type with the handler. With that the handler is called if event occurs.
        :param event_type: Pygame event
        :param handler: Implements a method that is performed when the event occurs.
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type: EventType, handler: Callable[[], None]) -> bool:
        """
        Unsubscribe a handler from a certain event_type.
        :param event_type: Pygame event
        :param handler: Implements a method that is performed when the event occurs.
        :returns: Bool if unregistration was successful
        """
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)
            if not self.handlers[event_type]:
                del self.handlers[event_type]
            return True
        else:
            return False

    def dispatch(self, event_type: EventType) -> None:
        """
        Notify all observers of the event_type that the event occurred.
        :param event_type: Pygame event
        """
        for handler in self.handlers[event_type]:
            handler(event_type)

    def get_events(self):
        """
        Go through all events that occurred and dispatch the functions handling the events.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dispatch(EventType.GAME_QUIT)

            if event.type == pygame.KEYDOWN:
                # Game running events
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.dispatch(EventType.INPUT_EVENT.UP)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.dispatch(EventType.INPUT_EVENT.RIGHT)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.dispatch(EventType.INPUT_EVENT.DOWN)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.dispatch(EventType.INPUT_EVENT.LEFT)

                # Title screen events
                elif event.key == pygame.K_SPACE:
                    self.dispatch(EventType.START_GAME)

from typing import Dict, List, Callable, TypeVar

import pygame

from event_handling.event_types import Event, GameQuitEvent, StartGameEvent, MovementEvent
from defs import Direction

class EventManager:
    E = TypeVar("E", bound = Event)
    EventHandler = Callable[[E], None] # Function/Method dealing with the input event.
    handlers: Dict[type[Event], List[EventHandler]]
    # Handlers are registered and build the connection between an event_type and the function handling the event.

    def __init__(self):
        self.handlers = {}

    def register(self, event_type: type[E], handler: EventHandler[E]) -> None:
        """
        Subscribe a handler to a certain event_type.
        This links the event_type with the handler. With that the handler is called if event occurs.
        :param event_type: Pygame event
        :param handler: Implements a method that is performed when the event occurs.
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type: type[E], handler: EventHandler[E]) -> bool:
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

    def dispatch(self, event: Event) -> None:
        """
        Notify all observers of the event_type that the event occurred.
        :param event: Pygame event
        """
        event_type = type(event)
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                handler(event)

    def get_events(self):
        """
        Go through all events that occurred and dispatch the functions handling the events.
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dispatch(GameQuitEvent())

            if event.type == pygame.KEYDOWN:
                # Game running events
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.dispatch(MovementEvent(Direction.NORTH))
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.dispatch(MovementEvent(Direction.EAST))
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.dispatch(MovementEvent(Direction.SOUTH))
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.dispatch(MovementEvent(Direction.WEST))

                # Title screen events
                elif event.key == pygame.K_SPACE:
                    self.dispatch(StartGameEvent())

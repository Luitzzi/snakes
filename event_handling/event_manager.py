from typing import Dict, List

from event_types import EventType
from event_handlers.event_handler import EventHandler

class EventManager:
    handlers: Dict[EventType, List[EventHandler]]

    def __init__(self):
        self.handlers = {}

    def register(self, event_type: EventType, handler: EventHandler) -> None:
        """
        Subscribe a handler to a certain event_type.
        This links the event_type with the handler. With that the handler is called if event occurs.
        :param event_type: Pygame event
        :param handler: Implements a method that is performed when the event occurs.
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unregister(self, event_type: EventType, handler: EventHandler) -> bool:
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
            handler.handle_event(event_type)


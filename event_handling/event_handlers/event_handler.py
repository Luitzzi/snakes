from abc import ABC, abstractmethod

from event_handling.event_types import EventType

class EventHandler(ABC):
    """
    Interface for all event handlers
    """

    @abstractmethod
    def handle_event(self, event_type: EventType) -> None:
        """Handle a certain event when it is dispatched"""

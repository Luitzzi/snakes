from typing import override

import pygame

from event_handling.event_handlers.event_handler import EventHandler
from event_handling.event_types import EventType


class QuitHandler(EventHandler):

    @override
    def handle_event(self, event_type: EventType) -> None:
        print("Closing game...")
        pygame.quit()
        exit()

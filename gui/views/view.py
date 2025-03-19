import pygame
from abc import ABC, abstractmethod


class View(ABC):
    """
    abstract class
    """

    surf: pygame.Surface

    @abstractmethod
    def capture(self) -> pygame.Surface:
        pass

import pygame
from game.game import Game


def main():
    pygame.init()
    game = Game(12, 12)
    game.run()


if __name__ == "__main__":
    main()

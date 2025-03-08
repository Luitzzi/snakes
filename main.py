import pygame
from game_utils.game import Game


def main():
    pygame.init()
    game = Game(20,20)
    game.run()


if __name__ == "__main__":
    main()

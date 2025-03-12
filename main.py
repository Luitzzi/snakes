import pygame
from game_utils.game import Game
from ai.game_ai import GameAI


def main():
    pygame.init()
    game = Game(5,5)
    game.run()


if __name__ == "__main__":
    main()

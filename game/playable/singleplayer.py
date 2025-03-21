from typing import override, List

import pygame

from game.game_objects.food_logic import FoodLogic
from game.game_state import GameState
from game.playable.playable import Playable
from game.player.player import Player
from game.player.humanplayer import HumanPlayer

class Singleplayer(Playable):
    """
    Game-mode Singleplayer:
    One Human plays against multiple optional enemies.
    The enemies can be controlled by an AI-Agent or Algorithm.
    The Player objects have the SnakeLogic as an Attribute,
    while the food is handled at the Singleplayer-class level.
    """
    time_alive: int
    score: int

    player: HumanPlayer
    enemies: List[Player]
    field_size: tuple[int, int]
    food_logic: FoodLogic

    def __init__(self, player: Player, enemies: List[Player], field_size: tuple[int, int]):
        self.time_alive = None
        self.score = None

        self.player = player
        self.enemies = enemies
        self.field_size = field_size

        self.food_logic = FoodLogic(self.field_size)
        # TODO: Implement that the food can't spawn in the body of any snake.

    @override
    def play_step(self) -> GameState:
        """
        Update the game-state:
        - Execute all actions: Of the real player as well as all computer-agents.
        - Check if any snake ate the food
        - Check if any snake collided and update the is_alive attribute
          of the SnakeLogic inside the corresponding Player.
        - Check if a snake ate the food and update everything accordingly.
        """
        self.execute_all_actions()
        self.handle_eating()
        new_game_state = self.check_for_collisions()
        return new_game_state

    def execute_all_actions(self) -> None:
        self.player.execute_action()

        for enemy in self.enemies:
            action = enemy.get_action()
            enemy.execute_action(action)

    def handle_eating(self) -> None:
        for snake in self.player or self.enemies:
            if snake.did_eat(self.food_logic.location):
                self.food_logic.respawn()

    def check_for_collisions(self) -> GameState:
        """
        Check first if the player collided. This would end the game.
        Then check if any enemy collided. On collision the is_alive attribute
        of the player is set to False.
        Because of that it the Player won't perform any play_steps anymore.
        :return: State of the game. If collision occurred: GAME_OVER, else PLAYING.
        """
        if self.player.is_collision(self.field_size):
            self.time_alive = self.get_time_alive()
            return GameState.GAME_OVER

        for enemy in self.enemies:
            enemy.is_collision(self.field_size) # TODO: Implement respawn timer. Currently the snake just stays dead.
        return GameState.PLAYING

    def get_time_alive(self) -> int:
        """
        Returns how long the player is playing in the game_active state
        :return: int representing the time in seconds
        """
        if self.time_alive is None:
            return None
        else:
            running_time_millis = pygame.time.get_ticks() - self.time_alive
            return running_time_millis // 1000
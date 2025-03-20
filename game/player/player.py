from abc import ABC, abstractmethod

from game.game_objects.direction import Direction
from game.game_objects.snake_logic import SnakeLogic

class Player(ABC):
    """
    Interface for a Player playing on a Playable-Object.
    A Player can be a Human, AIAgent, Algorithm etc.
    Each Player has its own SnakeLogic keeping track of the direction and
    all aspects of the game.
    """
    snake_logic: SnakeLogic
    is_alive: bool

    @abstractmethod
    def get_action(self) -> Direction:
        """
        Get the action the player performs at the current state of the game
        :return: Chosen action in the form of the new direction the snake should move.
        """

    @abstractmethod
    def execute_action(self, action):
        """
        Execute the action on the SnakeLogic if the snake is alive.
        :param action:
        :return:
        """

    def is_collision(self, field_size: tuple[int, int]) -> bool:
        """
        Checks if the snake collided with the field border or a snake body.
        :param field_size:
        :return: If collision occurred: True, else: False
        """
        new_head = self.snake_logic.get_head()
        if (
                new_head in self.snake_logic.body[1:]
                or new_head[0] < 0
                or new_head[0] >= field_size[0]
                or new_head[1] < 0
                or new_head[1] >= field_size[1]
        ):
            self.is_alive = False
            return True
        else:
            return False

    def did_eat(self, food_position):
        """
        Check if the new head of the snake is on the position of the food.
        If this is True, the snake grows by one -> The tail is not cut.
        Else: The tail position of the last tick stays. Due to the fact that the
        head of the snake moves the snake grows.
        :param food_position:
        :return: Snake_ate: True, else: False
        """
        new_head = self.snake_logic.get_head()
        if new_head == food_position:
            return True
        else:
            self.snake_logic.body.pop()
            return False

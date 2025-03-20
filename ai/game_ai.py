import pygame

import config
import ai.ai_config as ai_config
from gui import GUI
from game_utils.food_logic import FoodLogic
from sprites.food_sprite import FoodSprite
from game_utils.snake_logic import SnakeLogic
from sprites.snake_sprite import SnakeSprite
from game_utils.direction import Direction

class GameAI:

    def __init__(self, field_width, field_height):
        # Setup field settings
        self.gui = GUI(field_width, field_height, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.clock = pygame.time.Clock()

        self.num_episodes = 0
        self.reset()

    def reset(self):
        self.terminated = False
        self.frame_iteration = 0
        self.score = 0

        """
        direction enables the snake agent to take an action from the perspective of the snake.
        direction[direction_idx] = current_direction.
        Left turn: idx++
        Right turn: idx--
        """
        self.direction = [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
        self.direction_idx = 0
        self.snake_ate = False

        # Setup game elements
        self.snake_starting_position = config.calc_starting_position(self.gui.field_width, self.gui.field_height)
        self.snake_logic = SnakeLogic(self.snake_starting_position)
        self.snake_sprite = SnakeSprite(self.gui, self.snake_logic)
        self.food_logic = FoodLogic(self.snake_starting_position, self.gui.field_width, self.gui.field_height)
        self.food_sprite = FoodSprite(self.gui, self.food_logic)

    def play_step(self, action):
        """
        Execute the action the agent chose.
        :param action: turn_left, stay_straight, or turn_right
        :return: Reward for the chosen action: Snake died = -10; Snake ate = 10; Else = 0
        """
        self.frame_iteration += 1

        self.__update_direction(action)
        self.__handle_eating()
        self.terminated = self.__execute_action()
        reward = self.__calc_reward()
        self.__draw()
        return reward

    def get_current_direction(self):
        return self.direction[self.direction_idx]

    def get_turn_directions(self):
        """
        Converts the direction represented by a list [east, north, west, south]
        and the direction_idx showing the current direction to the actual geographic
        directions the snake would move when executing an action.
        :return: Dictionary in the form of: {
                 "left_turn_direction": left_turn_direction,
                 "straight_direction": straight_direction,
                 "right_turn_direction": right_turn_direction }
        """
        straight_direction = self.direction[self.direction_idx]
        left_turn_direction = self.direction[(self.direction_idx + 1) % len(self.direction)]
        right_turn_direction = self.direction[(self.direction_idx - 1) % len(self.direction)]
        return {
            "left_turn_direction": left_turn_direction,
            "straight_direction": straight_direction,
            "right_turn_direction": right_turn_direction
        }

    def __update_direction(self, action):
        """
        Update the moving direction in the snake instance.
        :param action (AgentAction): turn_eft, turn_right or turn_straight
        """
        match action:
            case [1, 0, 0]:
                self.direction_idx += 1
            case [0, 0, 1]:
                self.direction_idx -= 1
            case [0, 1, 0]:
                pass

        # Squash the index into the length of the direction list
        self.direction_idx = self.direction_idx % len(self.direction)

        new_direction = self.direction[self.direction_idx]
        self.snake_logic.set_direction(new_direction)

    def __execute_action(self):
        """
        :return: True if the game has terminated
        """
        self.snake_logic.move()

        if self.is_collision() or self.__terminated_by_frame_iteration():
            return True
        else:
            return False

    def is_collision(self, position = None):
        """
        Check if the position results in a collision.
        :return: bool: True if collision occurred, False if not
        """
        if position is None:
            # Check is the new_head of the snake collides
            position = self.snake_logic.get_head()

        if (
            position in self.snake_logic.body[1:]
            or position[0] < 0
            or position[0] >= self.gui.field_width
            or position[1] < 0
            or position[1] >= self.gui.field_height
        ):
            return True
        else:
            return False

    def __terminated_by_frame_iteration(self):
        """
        Check if the frame_iterations exceeds a certain value to stop the training iteration.
        This prevents the agent from stalling the game with just turning in a cycle.
        The multiplication ensures that the snake eats.
        """
        if self.frame_iteration > 50 * len(self.snake_logic.body):
            return True
        else:
            return False

    def __calc_reward(self):
        """
        Calculate the reward the agent gets for its action
        :return: Snake died = -10; Snake ate = 10; Else = 0
        """
        if self.terminated:
            return ai_config.REWARD_TERMINATED
        if self.snake_ate:
            self.score += 1
            self.snake_ate = False
            return ai_config.REWARD_EATING
        else:
            return 0

    def __draw(self):
        pygame.draw.rect(self.gui.screen, config.FIELD_COLOR, self.gui.field_rect)
        self._draw_field_objects()
        pygame.display.flip()
        self.clock.tick(config.FPS)

    # TODO: Change to new drawer (Current redundant with game class)
    def _draw_field_objects(self):
        """
        Draw all objects located on the field.
        Snake, food.
        """
        self.snake_sprite.draw()
        self.food_sprite.draw()

    def __handle_eating(self):
        """
        Added: self.snake_ate = True
        Necessary for the __calc_reward method to determine the reward
        """
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.snake_ate = True
            self.food_logic.respawn(self.snake_logic.body)
        else:
            self.snake_logic.body.pop()

    @staticmethod
    def __handle_events():
        """
        No user inputs anymore.
        Only the check for QUIT is necessary.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

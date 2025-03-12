import pygame
from typing import override

import config
from ai.agent import Agent
from game_utils.game import Game
from game_utils.direction import Direction
from ai.agent_action import AgentAction
from game_utils.game_states import GameStates


class GameAI(Game):
    frame_iteration = 0

    def __init__(self, width, height):
        super().__init__(width, height)
        """
        self.direction enables the snake agent to take an action from the perspective of the snake.
        self.index_of_curr_direction (short idx) points to the element in the direction list
        in that the snake is currently moving.
        From the snake's perspective it can take a left (idx++) or right (idx--) turn.
        Afterwards the idx is taken % len(direction) to ensure that it is in the list's bounds.
        """
        self.direction = [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]
        self.index_of_curr_direction = 0

        self.snake_ate = False
        self.agent = Agent()

    @override
    def run(self):
        self.screen.fill(config.BG_COLOR)
        self.start_time = pygame.time.get_ticks()
        while self.game_running:
            self._handle_events()
            # ai-agent interaction
            self.play_step(AgentAction.stay_straight)
            # draw the game
            self._game_active_logic()
        pygame.quit()

    @override
    def _handle_events(self):
        """
        No user inputs anymore.
        Therefore, only the check for QUIT is necessary.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False

    @override
    def _game_active_logic(self):
        pygame.draw.rect(self.screen, config.FIELD_COLOR, self.gui.field_rect)
        self._draw()
        pygame.display.flip()
        self.clock.tick(config.FPS)

    @override
    def _handle_eating(self):
        """
        Added:
        If the snake eats set self.snake_ate to True
        This is necessary for the __calc_reward method to determine the reward
        :return:
        """
        new_head = self.snake_logic.get_head()
        if new_head == self.food_logic.location:
            self.snake_ate = True
            self.food_logic.respawn(self.snake_logic.body)
        else:
            self.snake_logic.body.pop()


    def reset(self):
        self.__init__(self.gui.field_width, self.gui.field_height)

    def play_step(self, action):
        """
        Execute the action the ai-agent chose.
        :param action (AgentAction): turn_left, turn_right or stay_straight
        :return: Reward for the chosen action: Snake died = -10; Snake ate = 10
                 is_running bool
        """
        self.frame_iteration += 1
        self.__update_direction(action)
        return self.__calc_reward(), self.game_running

    def get_turn_directions(self):
        straight_direction = self.direction[self.index_of_curr_direction]
        left_turn_direction = self.direction[(self.index_of_curr_direction + 1) % len(self.direction)]
        right_turn_direction = self.direction[(self.index_of_curr_direction - 1) % len(self.direction)]
        return straight_direction, left_turn_direction, right_turn_direction


    def __update_direction(self, action):
        """
        Update the direction the snake is moving.
        :param action (AgentAction): turn_eft, turn_right or turn_straight
        """
        match action:
            case AgentAction.turn_left:
                self.index_of_curr_direction += 1
            case AgentAction.turn_right:
                self.index_of_curr_direction -= 1
            case AgentAction.stay_straight:
                pass
        # Squash the index into the length of the direction list
        self.index_of_curr_direction = self.index_of_curr_direction % len(self.direction)

        # Update the direction in the snake instance
        new_direction = self.direction[self.index_of_curr_direction]
        self.snake_logic.set_direction(new_direction)

    def __calc_reward(self):
        """
        Calculate the reward the ai-agent gets for its action
        :return: Snake died = -10; Snake ate = 10
        """
        # Update the game
        self._update_state()
        if self._is_collision(self.snake_logic.get_head()):
            self.game_running = False
        self.__check_frame_iterations()

        # Calc reward
        if not self.game_running:
            return -10
        if self.snake_ate:
            self.snake_ate = False
            return 10

    def __check_frame_iterations(self):
        """
        Check if the frame_iterations exceeds a certain value to stop the training iteration.
        This prevents the agent from stalling the game with just turning in a cycle.
        The multiplication ensures that the snake eats, else wise the game ends earlier.
        """
        if self.frame_iteration > 50 * len(self.snake_logic.body):
            self.game_running = False

from collections import deque

import torch
import random
import numpy as np

from ai.model import Linear_Qnet, QTrainer
from game_utils.direction import Direction, add_position_tuples

MAX_MEMORY = 100_000
BATCH_SIZE = 1_000
LEARNING_RATE = 0.01
EPSILON_START = 80
UPPER_BOUND_RANDOM_MOVE = 200

INPUT_SIZE = 13 # 4 * danger, 4 * current_direction, 4 * food_direction, is_running
HIDDEN_SIZE = 256
OUTPUT_SIZE = 3

class Agent:

    def __init__(self):
        self.count_games = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # Discount rate
        self.memory = deque(maxlen = MAX_MEMORY) # Stores the state, action, reward, next_state and done as one tuple
        self.model = Linear_Qnet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        """
        Returns the current state of the environment (11 values in a list)
        :param game:
        :return: Numpy array of bools (as int 0/1):
            [is_danger_left, is_danger_straight, is_danger_right  -dangerous positions
             north, east, south, west,  -current_direction
             north, east, south, west]  -food_direction
        """
        danger_positions = self.__get_danger_positions(game)
        current_direction = self.__get_current_direction(game)
        food_direction = self.__get_direction_of_food(game)

        state = danger_positions + current_direction + food_direction
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, is_running):
        self.memory.append((state, action, reward, next_state, is_running))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, are_running = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, are_running)

    def train_short_memory(self, state, action, reward, next_state, is_running):
        """
        Trains only on one step
        :param state:
        :param action:
        :param reward:
        :param next_state:
        :return:
        """
        self.trainer.train_step(state, action, reward, next_state, is_running)

    def get_action(self, state):
        """
        Returns the action the agent takes.
        This can either be a random move with a set probability from epsilon,
        or based on the neural-network-model.
        :param state:
        :return: List with bools ( as int 0/1): [turn_left, stay_straight, turn_right]
        """
        self.epsilon = EPSILON_START - self.count_games
        '''
        Epsilon ensures making random moves at the beginning:
        Tradeoff between exploration and exploitation.
        The more games a played the smaller epsilon gets.
        '''
        final_move = [0, 0, 0]
        if random.randint(0, UPPER_BOUND_RANDOM_MOVE) < self.epsilon:
            # Random move
            move = random.randint(0, len(final_move))
            final_move[move] = 1
        else:
            # Move based on model
            state_torch = torch.tensor(state, dtype = torch.float32)
            prediction = self.model(state_torch)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    @staticmethod
    def __get_danger_positions(game):
        """
        Check if there is a danger (collision for any possible action
        :return: List with bools in the form of: [is_danger_straight, is_danger_left, is_danger_right]
        """
        straight_direction, left_turn_direction, right_turn_direction = game.get_turn_directions()
        snake_head = game.snake_logic.get_head()
        straight_position = add_position_tuples(snake_head, straight_direction)
        left_turn_position = add_position_tuples(snake_head, left_turn_direction)
        right_turn_position = add_position_tuples(snake_head, right_turn_direction)

        is_danger_straight = game._is_collision(straight_position)
        is_danger_left = game._is_collision(left_turn_position)
        is_danger_right = game._is_collision(right_turn_position)

        return [is_danger_left, is_danger_straight, is_danger_right]

    @staticmethod
    def __get_current_direction(game):
        """
        Returns the current direction in that the snake is moving
        :param game:
        :return: List of bools in the form of: [north, east, south, west]
        """
        current_direction = game.snake_logic.direction
        north = False
        east = False
        south = False
        west = False
        match current_direction:
            case Direction.NORTH:
                north = True
            case Direction.EAST:
                east = True
            case Direction.SOUTH:
                south = True
            case Direction.WEST:
                west = True

        return [north, east, south, west]

    def __get_direction_of_food(self, game):
        """
        Returns the direction in that the food is located.
        :param game:
        :return: List of bools in the form of: [north, east, south, west]
        """
        position_head = game.snake_logic.get_head()
        position_food = game.food_logic.location

        north = position_head[1] > position_food[1]
        south = position_head[1] < position_food[1]
        east = position_head[0] < position_food[0]
        west = position_head[0] > position_food[0]

        return [north, east, south, west]



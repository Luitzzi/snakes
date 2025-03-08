from itertools import chain
from collections import deque

import torch
import random
import numpy as np

from model import Linear_Qnet, QTrainer
from game_utils.direction import Direction

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
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
        self.memory = deque(maxlen = MAX_MEMORY) # Stores the state, action, reward, next_state and done as one tupel
        self.model = Linear_Qnet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        """
        Returns the current state of the environment
        :param game:
        :return: Numpy array of bools (as int 0/1):
            [danger_north, danger_east, danger_south, danger_west,  -danger_position
             north, east, south, west,  -current_direction
             north, east, south, west,  -food_direction
             is_running]  -is game running
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


    def __get_danger_positions(self, game):
        """
        Check if there is a danger (collision) at any adjacent field of the snake's head.
        :param game:
        :return: List with bools in the form of: [danger_north, danger_east, danger_south, danger_west]
        """
        snake_head = game.snake_logic.body[0]
        # Possible danger position
        north_of_snake_head = snake_head + Direction.up
        east_of_snake_head = snake_head + Direction.right
        south_of_snake_head = snake_head + Direction.down
        west_of_snake_head = snake_head + Direction.left
        # Check danger positions
        current_direction = game.snake_logic.direction
        danger_north = False
        danger_east = False
        danger_south = False
        danger_west = False
        match current_direction:
            case Direction.left:
                danger_north = game._is_collision(north_of_snake_head)
                danger_south = game._is_collision(south_of_snake_head)
                danger_west = game._is_collision(west_of_snake_head)
            case Direction.right:
                danger_north = game._is_collision(north_of_snake_head)
                danger_east = game._is_collision(east_of_snake_head)
                danger_south = game._is_collision(south_of_snake_head)
            case Direction.up:
                danger_north = game._is_collision(north_of_snake_head)
                danger_east = game._is_collision(east_of_snake_head)
                danger_west = game._is_collision(west_of_snake_head)
            case Direction.down:
                danger_east = game._is_collision(east_of_snake_head)
                danger_south = game._is_collision(south_of_snake_head)
                danger_west = game._is_collision(west_of_snake_head)

        return [danger_north, danger_east, danger_south, danger_west]

    def __get_current_direction(self, game):
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
            case Direction.up:
                north = True
            case Direction.right:
                east = True
            case Direction.down:
                south = True
            case Direction.left:
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



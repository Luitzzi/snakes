from collections import deque

import torch
import random
import numpy as np

import ai.ai_config as ai_config
from ai.model import LinearQnet
from ai.trainer import QTrainer
from game_utils.direction import Direction, add_position_tuples

class Agent:

    def __init__(self, game):
        self.memory = deque(maxlen = ai_config.MAX_MEMORY)
        self.model = LinearQnet(ai_config.INPUT_SIZE, ai_config.HIDDEN_SIZE, ai_config.OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, ai_config.LEARNING_RATE, ai_config.GAMMA)

        self.game = game
        self.epsilon = self.__calc_epsilon()

    def safe_experience(self, state, action, reward, next_state, terminated):
        """
        Safes the experience of a step in a tuple:
        (state, action, reward, next_state, done)
        :param state: State of the environment before the action was executed
        :param action: Action performed on the state
        :param reward: Reward received for the action
        :param next_state: Resulting new state after taking the action
        :param terminated: Represents if the episode is done, therefore terminated
        """
        self.memory.append((state, action, reward, next_state, terminated))

    def train_short_memory(self, state, action, reward, next_state, terminated):
        """
        Trains on only one move. (Temporal difference learning)
        Performed always after a play_step
        :param state: State of the environment before the action was executed
        :param action: Action performed on the state
        :param reward: Reward received for the action
        :param next_state: Resulting new state after taking the action
        :param terminated: Is episode terminated
        """
        self.trainer.train_step(state, action, reward, next_state, terminated)

    def train_long_memory(self):
        """
        Experience training:
        Sample a batch from the memory and retrain on it.
        Breaks correlations between sequential experiences and improves stability.
        """
        if len(self.memory) > ai_config.BATCH_SIZE:
            mini_sample = random.sample(self.memory, ai_config.BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, done = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, done)

    def get_state(self):
        """
        Returns the current state of the environment as a numpy array
        with 11 values:
        [is_danger_left, is_danger_straight, is_danger_right
         north, east, south, west, <- current direction
         north, east, south, west] <- food direction
        :return: numpy array of bools represented by 0 and 1 with 11 values
        """
        danger_positions = self.__get_danger_positions()
        current_direction = self.__get_current_direction()
        food_direction = self.__get_direction_of_food()

        state = danger_positions + current_direction + food_direction
        return np.array(state, dtype=int)

    def get_action(self, state):
        """
        Uses the epsilon-greedy policy to determine the best action for the given state.
        :param state: numpy array of bools represented by 0 and 1 with 11 values.
                      It is a discrete state
        :return: action the model predicted
        """
        self.epsilon = self.__calc_epsilon()
        final_move = [0, 0, 0]
        random_num = random.uniform(0, 1)
        if random_num > self.epsilon:
            # Exploitation -> Model predicts the move
            state_torch = torch.tensor(state, dtype = torch.float32)
            prediction = self.model(state_torch)
            move_idx = torch.argmax(prediction).item()
        else:
            # Exploration -> Random move
            move_idx = random.randint(0, len(final_move) - 1)

        final_move[move_idx] = 1
        return final_move

    def __calc_epsilon(self):
        """
        Calculate the epsilon (randomness). Exponential decay using the decay rate.
        ε = min + (max - min) * exp(-decay * num_episodes)
        """
        return (ai_config.EPSILON_MIN + (ai_config.EPSILON_MAX - ai_config.EPSILON_MIN)
         * np.exp(-ai_config.EPSILON_DECAY * self.game.num_episodes))

    def __get_danger_positions(self):
        """
        Check if a possible action would result in a collision
        :return: List with bools in the form of:
                 [is_danger_straight, is_danger_left, is_danger_right]
        """
        turn_directions = self.game.get_turn_directions()
        snake_head = self.game.snake_logic.get_head()
        # Calculate the position on the field the snake would land doing a certain turn
        left_turn_field = add_position_tuples(snake_head, turn_directions["left_turn_direction"])
        straight_field = add_position_tuples(snake_head, turn_directions["straight_direction"])
        right_turn_field = add_position_tuples(snake_head, turn_directions["right_turn_direction"])
        # Check if at such a position a collision would occur
        is_danger_straight = self.game.is_collision(straight_field)
        is_danger_left = self.game.is_collision(left_turn_field)
        is_danger_right = self.game.is_collision(right_turn_field)

        return [is_danger_left, is_danger_straight, is_danger_right]

    def __get_current_direction(self):
        """
        Returns the current direction in that the snake is moving
        :return: List of bools in the form of: [north, east, south, west]
        """
        current_direction = self.game.get_current_direction()
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

    def __get_direction_of_food(self):
        """
        Returns the direction in that the food is located.
        :return: List of bools in the form of: [north, east, south, west]
        """
        position_head = self.game.snake_logic.get_head()
        position_food = self.game.food_logic.location

        north = position_head[1] > position_food[1]
        south = position_head[1] < position_food[1]
        east = position_head[0] < position_food[0]
        west = position_head[0] > position_food[0]

        return [north, east, south, west]


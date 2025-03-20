import torch
import torch.nn as nn
import torch.optim as optim

class QTrainer:
    """
    Implements the learning functionality for the nn and handles experience replay.
    """

    def __init__(self, model, learning_rate, gamma):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.learning_rate)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, terminated):
        """
        Train the nn on the data from one or multiple play_steps.
        The parameters are either single values or a list/2D tensor consisting of a randomly selected batch
        from the experience memory.
        :param state: State of the environment before the action was executed
        :param action: Action performed on the state
        :param reward: Reward received for the action
        :param next_state: Resulting new state after taking the action
        :param terminated: Is episode terminated
        """
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)

        if len(state.shape) == 1:
            # Handle single-step case
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            next_state = torch.unsqueeze(next_state, 0)
            terminated = (terminated,)

        target, prediction = self.__update_Q_value(state, action, reward, next_state, terminated)
        self.__perform_backpropagation(target, prediction)

    def __update_Q_value(self, state, action, reward, next_state, terminated):
        predicted_Q = self.model(state)
        target = predicted_Q.clone()

        for idx in range(len(state)):
            if terminated[idx]:
                new_Q = reward[idx]
            else:
                # Bellman equation: Q(s,a) = R + γ * argmax Q'(s',a')
                new_Q = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = new_Q # Replace the taken action with the new Q value
        return target, predicted_Q

    def __perform_backpropagation(self, target, prediction):
        self.optimizer.zero_grad()
        loss = self.criterion(target, prediction) # The action that were not taken cancel out
        loss.backward()
        self.optimizer.step()

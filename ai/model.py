import os

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class Linear_Qnet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:

    def __init__(self, model, learning_rate, gamma):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.learning_rate)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, is_running):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(state, 0)
            reward = torch.unsqueeze(state, 0)
            is_running = (is_running, )

        predicted_Q = self.model(state)
        target = predicted_Q.clone()
        for idx in range(len(is_running)):
            Q_new = reward[idx]
            if is_running[idx]:
                Q_new = reward + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx] [torch.argmax(action).item] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, predicted_Q)
        loss.backward()
        self.optimizer.step()


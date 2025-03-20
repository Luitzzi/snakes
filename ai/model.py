import os

import torch
import torch.nn as nn
import torch.nn.functional as F

import config

class LinearQnet(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Saves the model with its state_dict.
        :param file_name:
        """
        if not os.path.exists(config.SAVE_MODEL_PATH):
            os.makedirs(config.SAVE_MODEL_PATH)

        file_name = os.path.join(config.SAVE_MODEL_PATH, file_name)
        torch.save(self.state_dict(), file_name)


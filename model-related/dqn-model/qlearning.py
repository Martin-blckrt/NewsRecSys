# -*- coding: utf-8 -*-
######################################################################
# Full details on
# https://github.com/pytorch/tutorials/blob/master/intermediate_source/reinforcement_q_learning.py
######################################################################
import random
from collections import deque

from constants import *  # toto made file.py

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.batch_size = BATCH_SIZE
        self.memory = deque([], maxlen=self.capacity)

    def __len__(self) -> int:
        return len(self.memory)

    def push(self, *args: Episode):
        self.memory.append(Episode(*args))

    def sample(self, batch_size) -> list:
        return random.sample(self.memory, batch_size)


class DQN(nn.Module):
    def __init__(self, input_size: int, output_size: int) -> None:
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.fc3 = nn.Linear(HIDDEN_SIZE, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.to(device)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=-1)
        return x


def optimize_model(
        memory: ReplayMemory, policy_net: DQN, target_net: DQN, optimizer: torch.optim, out_size: int) -> None:

    if len(memory) < BATCH_SIZE:
        return

    episodes = memory.sample(BATCH_SIZE)
    batch = Episode(*zip(*episodes))

    state_batch = torch.cat(batch.state).reshape(BATCH_SIZE, -1)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward).reshape(BATCH_SIZE, -1).expand(-1, out_size).reshape(-1)
    next_state_batch = torch.cat(batch.next_state).reshape(BATCH_SIZE, -1)

    state_action_values = (
        policy_net(state_batch)
        .gather(1, action_batch.type(torch.int64).unsqueeze(0))
        .squeeze(0)
    )
    next_state_values = target_net(next_state_batch).reshape(-1)
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    criterion = nn.SmoothL1Loss()

    loss = criterion(state_action_values, expected_state_action_values)

    optimizer.zero_grad()

    loss.backward()
    for param in policy_net.parameters():
        param.grad.data.clamp_(-1, 1)

    optimizer.step()

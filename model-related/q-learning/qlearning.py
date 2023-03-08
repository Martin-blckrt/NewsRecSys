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
    def __init__(self) -> None:
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.fc3 = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.to(device)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x), dim=-1)
        return x

#TODO: make these variables dynamic and how to init state
# Get number of actions from action space
n_actions = NB_OF_CATEGORIES
# Get the number of state observations
state = INITIAL_STATE
n_observations = len(state)

policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)

memory = ReplayMemory(MEMORY_SIZE)


def select_action(curr_state):
    # blurg
    return curr_state


def optimize_model():
    #TODO: study github version of this function
    if len(memory) < BATCH_SIZE:
        return
    episodes = memory.sample(BATCH_SIZE)

    batch = Episode(*zip(*episodes))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                       if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)

    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]

    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

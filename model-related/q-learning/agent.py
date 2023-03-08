import numpy as np
import torch
from constants import Episode, EPS_START, EPS_END, EPS_DECAY
from qlearning import DQN, device


class Agent:

    def __init__(self, action_space: list) -> None:
        self.epsilon_start = EPS_START
        self.epsilon_min = EPS_END
        self.epsilon_decay = EPS_DECAY

        self.step_counter = 0

        self.action_space = action_space
        self.action_count = {cat: 0 for cat in self.action_space}

        self.state, self.action, self.reward, self.next_state = None, None, None, None
        self.policy_net = DQN().to(device)

    def act(self, state: torch.Tensor):
        return

    def get_episode(
            self,
            state: np.ndarray = None,
            action: str = None,
            reward: int = None,
            next_state: np.ndarray = None,
    ) -> tuple:
        self.state, self.action, self.reward, self.next_state = (
            state, action, reward, next_state)

        episode = Episode(state, action, reward, next_state)

        return episode

    def __get_epsilon__(self):
        epsilon = max(
            self.epsilon_min,
            self.epsilon_start - self.step_counter / self.epsilon_decay,
        )
        self.step_counter += 1
        return epsilon

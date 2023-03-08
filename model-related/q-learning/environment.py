import pandas as pd
import numpy as np
import torch
from data_utils import load_dataset


class Environment:

    def __init__(self, *, local: bool = True):

        self.news_data = load_dataset(local)

    def get_state(self, user_id: str) -> torch.Tensor:

        return

    def get_action_space(self) -> list:
        return pd.unique(self.news_data['source'])

    def update_state(
            self, current_state: torch.Tensor, action: str, reward: torch.Tensor, user_id: str
    ) -> torch.Tensor:

        return

    def get_action_news_id(self, action) -> str:
        return

    def get_news_info(self, news_id: str) -> str:

        return

    def get_reward(self, user_input: int) -> torch.Tensor:
        if user_input == 1:
            return torch.tensor([1])
        elif user_input == -1:
            return torch.tensor([-1])

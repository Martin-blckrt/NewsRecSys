import pandas as pd
import numpy as np
import torch

from data_utils import load_dataset, load_history, sync_history
from constants import RANDOM_NEWS_RATE, STATE_WINDOW


class Environment:

    def __init__(self, *, user_id: str, local: bool = False):

        self.news_df = load_dataset(local)

        self.data_df = pd.get_dummies(self.news_df, columns=["source"])
        cols = list(self.news_df.columns)
        cols.remove("url")
        cols.remove("source")
        self.data_df = self.data_df.drop(cols, axis=1)

        self.user_id = user_id
        self.history = load_history(self.user_id, local)

        self.state_windows = STATE_WINDOW
        self.news_rand_rate = RANDOM_NEWS_RATE
        self.INPUT_SIZE = len(self.data_df.columns) - 2
        self.OUTPUT_SIZE = len(self.news_df)

    def get_input_size(self):
        return self.INPUT_SIZE

    def get_output_size(self):
        return self.OUTPUT_SIZE

    def get_state(self) -> torch.Tensor:

        last_k_news = self.history[-self.state_windows:]
        array = np.zeros((self.state_windows, self.INPUT_SIZE))

        for index, news_url in enumerate(last_k_news):
            values = self.data_df.loc[lambda df: df["url"] == news_url].values[0][1:-1]
            array[index] = values

        state = np.mean(array, axis=0)

        return torch.from_numpy(state).float()

    def get_action_space(self) -> list:
        return list(pd.unique(self.news_df["url"]))

    def update_state(self, current_state: torch.Tensor, reward: torch.Tensor) -> torch.Tensor:

        if reward[0].item() == 1:
            new_state = self.get_state()
            return new_state

        elif reward[0].item() == -1:
            new_state = current_state
            return new_state

    def update_history(self, recent: (str, list)) -> None:
        if isinstance(recent, list):
            self.history.extend(recent)
        else:
            self.history.append(recent)

    def synchronize_history(self, user_id) -> None:
        sync_history(user_id, self.history)

    def get_action_news(self, action_list: list) -> pd.DataFrame:

        return self.news_df.loc[self.news_df["url"].isin(action_list)]

    def get_reward(self, user_input: str) -> torch.Tensor:

        if user_input in self.history:
            return torch.tensor([1])
        else:
            return torch.tensor([0])

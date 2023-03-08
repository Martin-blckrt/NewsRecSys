import pandas as pd
import numpy as np
import itertools
import torch
from data_utils import load_dataset
from constants import RANDOM_NEWS_RATE, STATE_WINDOW, TOP_NEWS


class Environment:

    def __init__(self, *, local: bool = True):

        self.news_data = load_dataset(local)
        self.news_data.set_index('id', inplace=True)
        self.news_rand_rate = RANDOM_NEWS_RATE

    def get_state(self, user_id: str) -> torch.Tensor:

        return

    def get_action_space(self) -> list:
        """
        Les actions sont de la forme d'un choix de news (source, tag)
        :return: toutes combinaisons de source/tag
        """

        unique_sources = pd.unique(self.news_data['source'])
        unique_tags = pd.unique(self.news_data['tag'])

        return list(set(itertools.combinations([unique_sources, unique_tags], 2)))

    def update_state(
            self, current_state: torch.Tensor, action: str, reward: torch.Tensor, user_id: str
    ) -> torch.Tensor:

        return

    def get_action_news_id(self, action) -> str:

        random_news = np.random.uniform(0, 1) < self.news_rand_rate
        choice_df = self.news_data.loc[(self.news_data['source'] == action[0]) & (self.news_data['tag'] == action[1])]

        if random_news:
            result = choice_df.iloc[np.random.randint(0, choice_df.shape[0])]["id"]

        else:
            # TODO: check time stuff with clem/mart
            df = choice_df.sort_values(by=["_ts"], ignore_index=True, ascending=False)

            n_rows = df.shape[0]
            n_news = min(n_rows, TOP_NEWS)

            result = df["id"][0:n_news].values[np.random.randint(0, n_news)]

        return result

    def get_news_info(self, news_id: str):
        return self.news_data.loc[news_id]

    def get_reward(self, user_input: int) -> torch.Tensor:
        if user_input == 1:
            return torch.tensor([1])
        elif user_input == -1:
            return torch.tensor([-1])

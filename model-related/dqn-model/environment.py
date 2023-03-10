import pandas as pd
import numpy as np
import torch
from data_utils import load_dataset, load_history, sync_history
from constants import RANDOM_NEWS_RATE, STATE_WINDOW, TOP_NEWS


class Environment:

    def __init__(self, *, user_id: str, local: bool = True):

        self.news_data = load_dataset(local)
        self.history = load_history(user_id, local)
        self.news_data.set_index('id', inplace=True)
        self.news_rand_rate = RANDOM_NEWS_RATE

    def get_state(self, user_id: str) -> torch.Tensor:

        return

    def get_action_space(self) -> list:
        """
        Les actions sont de la forme d'un choix de source
        :return: toutes les valeurs différentes de source
        """

        unique_sources = pd.unique(self.news_data['source'])

        return list(set(unique_sources))

    def update_state(
            self, current_state: torch.Tensor, action: str, reward: torch.Tensor, user_id: str
    ) -> torch.Tensor:

        return

    def update_history(self, recent: (str, list)) -> None:
        if type(recent) == list:
            self.history.extend(recent)
        else:
            self.history.append(recent)

    def synchronize_history(self, user_id) -> None:
        sync_history(user_id, self.history)

    def get_action_news(self, action) -> list:

        random_news = np.random.uniform(0, 1) < self.news_rand_rate
        choice_df = self.news_data.loc[(self.news_data['source'] == action)]

        if random_news:
            result = choice_df.iloc[np.random.randint(0, choice_df.shape[0])]
        else:

            df = choice_df.sort_values(by=["_ts"], ignore_index=True, ascending=False)

            n_news = min(df.shape[0], TOP_NEWS)
            result = df.head(n_news)

        return result

    def get_reward(self, user_input: str) -> torch.Tensor:
        # TODO: from user_input (news ID), create the reward
        if user_input == 1:
            return torch.tensor([1])
        elif user_input == -1:
            return torch.tensor([-1])

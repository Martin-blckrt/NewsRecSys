import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import LabelEncoder

from data_utils import load_dataset, load_history, sync_history
from constants import RANDOM_NEWS_RATE, STATE_WINDOW, TOP_NEWS, INPUT_SIZE


class Environment:

    def __init__(self, *, user_id: str, local: bool = True):

        self.news_df = load_dataset(local)

        self.user_id = user_id
        self.history = load_history(self.user_id, local)

        self.label_encoder = None

        self.state_windows = STATE_WINDOW
        self.news_rand_rate = RANDOM_NEWS_RATE

    def get_state(self) -> torch.Tensor:

        last_k_news = self.history[-self.state_windows:]
        array = np.zeros((self.state_windows, INPUT_SIZE))  # INPUT_SIZE need study

        for index, news_id in enumerate(last_k_news):
            news = self.news_df.loc[self.news_df["id"] == news_id]
            news_source = news["source"]

            code = self.label_encoder.transform(news_source)
            array[index, code] += 1

        state = np.mean(array, axis=0)

        return torch.from_numpy(state).float()

    def get_action_space(self) -> list:

        unique_sources = list(pd.unique(self.news_df['source']))
        self.label_encoder = LabelEncoder().fit(unique_sources)

        return unique_sources

    def update_state(self, current_state: torch.Tensor, reward: torch.Tensor) -> torch.Tensor:

        if reward[0].item() == 1:

            self.update_history(self.news_df["id"])
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

    def get_action_news(self, action) -> list:

        random_news = np.random.uniform(0, 1) < self.news_rand_rate
        choice_df = self.news_df.loc[(self.news_df['source'] == action)]

        if random_news:
            result = choice_df.iloc[np.random.randint(0, choice_df.shape[0])]
        else:

            df = choice_df.sort_values(by=["_ts"], ignore_index=True, ascending=False)

            n_news = min(df.shape[0], TOP_NEWS)
            result = df.head(n_news)

        return result

    def get_reward(self, user_input: str) -> torch.Tensor:
        # TODO: from user_input (news ID), create the reward
        # idée ?
        # +1 si reco dans une source déjà déjà reco avant
        # +0 ou -1 si reco dans une source pas vues avant
        # ou alors -1 sur les news PAS cliquée mais nécessite de changer un peu le système
        if user_input == 1:
            return torch.tensor([1])
        elif user_input == -1:
            return torch.tensor([-1])

import pandas as pd
import numpy as np
import torch

from data_utils import load_dataset, load_history, sync_history
from constants import STATE_WINDOW


class Environment:

    def __init__(self, *, user_id: str, local: bool = False):

        self.user_id = user_id
        self.state_windows = STATE_WINDOW

        # récupération de l'historique de l'utilisateur
        self.history, self.state_history = load_history(self.user_id, local)

        # récupération du dataset sans les news déjà lues
        self.news_df = load_dataset(local)
        self.news_df = self.news_df[~self.news_df['url'].isin(self.history)]

        # encodage du dataset en binaire
        self.data_df = self.encode_news_df()

        # définition des tailles du modèle
        self.INPUT_SIZE = len(self.data_df.columns) - 1
        self.OUTPUT_SIZE = len(self.news_df)

    def encode_news_df(self):
        # encode df
        data_df = pd.get_dummies(self.news_df, columns=["source", "tag"])

        # gather all unwanted  columns, and remove the ones we keep
        cols_to_remove = list(self.news_df.columns)

        keep_col = ["url", "source", "tag"]
        for c in keep_col:
            cols_to_remove.remove(c)

        data_df = data_df.drop(cols_to_remove, axis=1)

        return data_df

    def get_input_size(self):
        return self.INPUT_SIZE

    def get_output_size(self):
        return self.OUTPUT_SIZE

    def get_state(self) -> torch.Tensor:

        last_k_news = self.history[-self.state_windows:]
        last_k_states = self.state_history[-self.state_windows:]

        array = np.zeros((self.state_windows, self.INPUT_SIZE))

        for index, (news_url, state_list) in enumerate(zip(last_k_news, last_k_states)):
            for state_val in state_list:
                for i, name in enumerate(self.data_df.columns[1:]):
                    array[index][i] = int(name == state_val)

        state = np.mean(array, axis=0)

        return torch.from_numpy(state).float()

    def get_action_space(self) -> list:
        return list(pd.unique(self.news_df["url"]))

    def update_state(self, current_state: torch.Tensor, reward: torch.Tensor) -> torch.Tensor:
        # mise à jour du state uniquement si l'article a été lu
        if reward[0].item() > 0:
            new_state = self.get_state()
            return new_state
        else:
            new_state = current_state
            return new_state

    def update_history(self, recent: str) -> None:

        self.history.append(recent)

        matching_df = self.data_df.loc[lambda df: df["url"] == recent]

        one_col = matching_df.apply(lambda row: row[row == 1], axis=1)

        self.state_history.append(list(one_col.columns))

    def synchronize_history(self, user_id) -> None:
        sync_history(user_id, self.history, self.state_history)

    def get_action_news(self, action_list: list) -> pd.DataFrame:
        return self.news_df.loc[self.news_df["url"].isin(action_list)]

    def get_sources(self, action_list: list):

        matches = self.data_df.loc[self.data_df["url"].isin(action_list)]
        one_col = matches.apply(lambda row: row[row == 1].index, axis=1)
        return [i.to_list() for i in one_col.to_list()]

import pandas as pd
import numpy as np
import torch

from data_utils import load_dataset, load_history, sync_history
from constants import STATE_WINDOW


class Environment:

    def __init__(self, *, user_id: str, local: bool = False):

        self.user_id = user_id
        self.state_windows = STATE_WINDOW

        self.history, self.state_history = load_history(self.user_id, local)

        self.news_df = load_dataset(local)

        self.data_df, nb_removed = self.encode_news_df()
        # self.news_df = self.news_df[~self.news_df['url'].isin(self.history)]

        self.INPUT_SIZE = len(self.data_df.columns) - nb_removed + 1
        self.OUTPUT_SIZE = len(self.news_df)

    def encode_news_df(self):
        # encode df
        data_df = pd.get_dummies(self.news_df, columns=["source"])

        # gather all unwanted  columns, and remove the ones we keep
        cols_to_remove = list(self.news_df.columns)

        keep_col = ["url", "source"]
        for c in keep_col:
            cols_to_remove.remove(c)

        data_df = data_df.drop(cols_to_remove, axis=1)

        # creates 'read_by_user' attribute after the last col
        data_df.insert(len(data_df.columns), "read_by_user", 0)

        # check all read news with a 1
        data_df.loc[data_df['url'].isin(self.history), 'read_by_user'] = 2

        return data_df, len(keep_col)

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

            array[index][-1] = self.data_df.loc[self.data_df["url"] == news_url].values[0][-1]

        state = np.mean(array, axis=0)

        return torch.from_numpy(state).float()

    def get_action_space(self) -> list:
        return list(pd.unique(self.news_df["url"]))

    def update_state(self, current_state: torch.Tensor, reward: torch.Tensor) -> torch.Tensor:
        if reward[0].item() > 0:
            new_state = self.get_state()
            return new_state
        else:
            new_state = current_state
            return new_state

    def update_history(self, recent: str) -> None:

        self.history.append(recent)

        self.data_df.loc[self.data_df["url"] == recent, 'read_by_user'] = 2
        matching_df = self.data_df.loc[lambda df: df["url"] == recent]

        one_col = matching_df.apply(lambda row: row[row == 1], axis=1)

        self.state_history.append(list(one_col.columns))

    def synchronize_history(self, user_id) -> None:
        sync_history(user_id, self.history, self.state_history)

    def get_action_news(self, action_list: list) -> pd.DataFrame:
        return self.news_df.loc[self.news_df["url"].isin(action_list)]

    def get_reward(self, user_input: str) -> torch.Tensor:
        if user_input in self.history:
            return torch.tensor([-1])
        else:
            return torch.tensor([1])

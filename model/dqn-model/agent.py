import numpy as np
import torch
from constants import Episode, EPS_START, EPS_END, EPS_DECAY, NEWS_NUMBER
from qlearning import DQN, device


class Agent:

    def __init__(self, action_space: list, input_size: int, output_size: int) -> None:
        # contrôle de l'exploration
        self.epsilon_start = EPS_START
        self.epsilon_min = EPS_END
        self.epsilon_decay = EPS_DECAY

        self.step_counter = 0

        self.action_space = action_space
        self.action_count = {tup: 0 for tup in self.action_space}

        self.state, self.action, self.reward, self.next_state = None, None, None, None
        self.policy_net = DQN(input_size, output_size).to(device)

    def act(self, state: torch.Tensor) -> tuple:

        action_news = []
        random_count = 0

        # calcul du nombre de news random
        for _ in range(NEWS_NUMBER):
            random_count += (np.random.uniform(0, 1) < self.__get_epsilon__())

        # prédiction du modèle
        with torch.no_grad():
            action_tensor = self.policy_net(state)

        random_indices = torch.randint(low=0, high=len(self.action_space), size=(random_count,))
        for index in random_indices:
            action_tensor[index] = 1

        # récupération des meilleures news
        action_indices = torch.topk(action_tensor, NEWS_NUMBER).indices
        temp = []
        for index in action_indices:
            temp.append(action_tensor[index])
            action_n = self.action_space[index]
            action_news.append(action_n)
            self.action_count[action_n] += 1

        return action_news, action_tensor, temp

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

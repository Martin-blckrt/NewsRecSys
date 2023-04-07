import os.path

import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.optim as optim
from constants import TARGET_UPDATE, MEMORY_SIZE, TAU, Episode
from qlearning import DQN, device, ReplayMemory, optimize_model
from agent import Agent
from environment import Environment
from metrics import avg_metric, similarity


class Model:
    def __init__(self) -> None:
        # target update parameter
        self.target_update = TARGET_UPDATE

        # None because we wait for 'login_user' method
        self.memory = None
        self.env = None
        self.agent = None
        self.policy_net = None
        self.target_net = None
        self.optimizer = None

        self.user_id = None
        self.state = None
        self.action_tensor = None
        self.action_news = None

        self.output_size = None
        self.list_eps = None
        self.avg_rewards = None
        self.sim_scores = None
        self.iter_counter = 0
        self.reward_cum_sum = 0

    def login_user(self, user_id: str, local: bool = False):

        if user_id is None:
            print("User is None !")
            raise TypeError
        else:
            print("User ID is", user_id)

        # does not reset vars if user is the same
        if self.user_id != user_id:
            self.user_id = user_id
            self.avg_rewards = []
            self.sim_scores = []
            self.iter_counter = 0

        """create env, agent, state, memory & networks"""
        self.memory = ReplayMemory(MEMORY_SIZE)
        self.env = Environment(user_id=user_id, local=local)

        input_size, self.output_size = self.env.get_input_size(), self.env.get_output_size()

        self.agent = Agent(self.env.get_action_space(), input_size, self.output_size)

        if os.path.exists(f"../user_models/{self.user_id}_policy"):
            self.agent.policy_net.load(self.user_id, name="policy")

        self.policy_net = self.agent.policy_net

        self.target_net = DQN(input_size, self.output_size).to(device)  # neural network here

        if os.path.exists(f"../user_models/{self.user_id}_target"):
            self.target_net.load(self.user_id, name="target")
        else:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        self.target_net.eval()

        self.state = None

        self.optimizer = optim.RMSprop(self.policy_net.parameters())

    def update_model(self):

        for eps in self.list_eps.values():
            self.memory.push(eps)

        optimize_model(self.memory, self.policy_net, self.target_net, self.optimizer, self.output_size)

        if self.iter_counter % self.target_update == 0:
            target_net_state_dict = self.target_net.state_dict()
            policy_net_state_dict = self.policy_net.state_dict()

            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[key] * TAU + target_net_state_dict[key] * (
                        1 - TAU)

            self.target_net.load_state_dict(target_net_state_dict)
    
    def update_metrics(self):
        self.avg_rewards.append(avg_metric(self.list_eps))

        reco_sources = self.env.get_sources(self.action_news)

        # méthode trimming but this function doesn't happen if len(hist) < 10
        state_hist = [j for state in self.env.state_history[-len(reco_sources):] for j in state]

        self.sim_scores.append(similarity(state_hist, reco_sources, method="jaccard"))

    def recommend_news(self, user_id) -> pd.DataFrame:

        if self.iter_counter != 0:
            self.quit()

            if len(self.env.state_history) >= len(self.action_news):
                self.update_metrics()

        self.login_user(user_id, local=False)

        self.state = self.env.get_state()
        self.action_news, self.action_tensor, temp = self.agent.act(self.state)

        reward = torch.tensor([-1])
        n_state = self.env.update_state(current_state=self.state, reward=reward)
        self.list_eps = {url: Episode(self.state, self.action_tensor, n_state, reward) for url in self.action_news}

        print("Iteration:", self.iter_counter)
        self.iter_counter += 1

        return self.env.get_action_news(self.action_news)

    def get_user_response(self, user_response: str) -> None:
        print("User Response is:", user_response)

        reward = torch.tensor([1])

        new_ep = self.list_eps[user_response]._replace(reward=reward)
        new_ep = new_ep._replace(next_state=self.env.update_state(current_state=self.state, reward=reward))

        self.list_eps[user_response] = new_ep

        self.env.update_history(user_response)

    def quit(self):
        self.update_model()

        self.policy_net.save(self.user_id, name="policy")
        self.target_net.save(self.user_id, name="target")
        self.env.synchronize_history(self.user_id)

    def plot_metrics(self):

        nb_data = self.iter_counter - 1

        if nb_data <= 0 or (len(self.env.state_history) < len(self.action_news)):
            print("Not enough data points or history data to plot")
            return

        iter_range = len(self.avg_rewards)

        # average reward
        plt.figure(figsize=(10, 8))
        plt.subplot(1, 2, 1)
        plt.plot(iter_range, self.avg_rewards, label='Average')
        plt.legend(loc='lower right')
        plt.title('Average reward by iterations')

        # similarity
        plt.subplot(1, 2, 2)
        plt.plot(iter_range, self.sim_scores, label='Similarity')
        plt.legend(loc='upper right')
        plt.title('Similarity by iterations')
        plt.show()

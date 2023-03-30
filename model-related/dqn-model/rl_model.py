import pandas as pd
import torch.optim as optim
from constants import TARGET_UPDATE, MEMORY_SIZE, Episode
from qlearning import DQN, device, ReplayMemory, optimize_model
from agent import Agent
from environment import Environment


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

            """create env, agent, state, memory & networks"""
            self.memory = ReplayMemory(MEMORY_SIZE)
            self.env = Environment(user_id=user_id, local=local)

            input_size, self.output_size = self.env.get_input_size(), self.env.get_output_size()

            self.agent = Agent(self.env.get_action_space(), input_size, self.output_size)

            self.policy_net = self.agent.policy_net
            self.target_net = DQN(input_size, self.output_size).to(device)  # neural network here
            self.target_net.load_state_dict(self.policy_net.state_dict())
            self.target_net.eval()

            self.state = None

            self.optimizer = optim.RMSprop(self.policy_net.parameters())

            self.iter_counter = 0
            self.reward_cum_sum = 0

    def recommend_news(self) -> pd.DataFrame:

        self.state = self.env.get_state()
        self.action_news, self.action_tensor, temp = self.agent.act(self.state)
        print(temp)
        return self.env.get_action_news(self.action_news)

    def get_user_response(self, user_response: str) -> None:
        print("User Response is:", user_response)

        reward = self.env.get_reward(user_response)

        self.env.update_history(user_response)

        next_state = self.env.update_state(current_state=self.state, reward=reward)

        self.memory.push(self.state, self.action_tensor, next_state, reward)
        optimize_model(self.memory, self.policy_net, self.target_net, self.optimizer, self.output_size)

        if self.iter_counter % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        self.reward_cum_sum += reward[0].item()

        print("Iteration:", self.iter_counter)
        self.iter_counter += 1

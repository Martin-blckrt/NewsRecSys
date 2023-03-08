import torch.optim as optim
from constants import TARGET_UPDATE, MEMORY_SIZE
from qlearning import DQN, device, ReplayMemory
from data_utils import load_dataset
from agent import Agent
from environment import Environment

class Model:
    def __init__(self, *, local: bool = True) -> None:
        """target update parameter"""
        self.target_update = TARGET_UPDATE

        """create env, agent, memory & networks"""
        self.env = Environment(local=local)

        self.agent = Agent(self.env.get_action_space())

        self.memory = ReplayMemory(MEMORY_SIZE)

        self.policy_net = self.agent.policy_net
        self.target_net = DQN().to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.RMSprop(self.policy_net.parameters())

        self.user_id = None
        self.state = None
        self.action_tensor = None
        self.action_news_id = None

        self.iter_counter = 0
        self.reward_cum_sum = 0

    def recommend_news(self, user_id: str) -> None:
        return

    def get_user_response(self, user_response: int) -> None:
        return

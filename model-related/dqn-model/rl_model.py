import torch.optim as optim
from constants import TARGET_UPDATE, MEMORY_SIZE, Episode
from qlearning import DQN, device, ReplayMemory, optimize_model
from agent import Agent
from environment import Environment


class Model:
    def __init__(self) -> None:
        # target update parameter
        self.target_update = TARGET_UPDATE

        # init memory
        self.memory = ReplayMemory(MEMORY_SIZE)

        # None because we wait for 'login_user' method
        self.env = None
        self.agent = None
        self.policy_net = None
        self.target_net = None
        self.optimizer = None

        self.user_id = None
        self.state = None
        self.action_tensor = None
        self.action_news = None

        self.iter_counter = 0
        self.reward_cum_sum = 0

    def login_user(self, user_id: str, local: bool = True):
        print("User ID is:", user_id)

        """create env, agent & networks"""
        self.env = Environment(user_id=user_id, local=local)

        self.agent = Agent(self.env.get_action_space())

        self.policy_net = self.agent.policy_net
        self.target_net = DQN().to(device)  # neural network here
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.RMSprop(self.policy_net.parameters())

    def recommend_news(self, user_id: str) -> list:
        print("User ID is:", user_id)

        self.user_id = user_id
        self.state = self.env.get_state(user_id)

        action_info, self.action_tensor = self.agent.act(self.state)
        self.action_news = self.env.get_action_news(action_info)

        return self.action_news

    def get_user_response(self, user_response: int) -> None:
        print("User Response is:", user_response)

        reward = self.env.get_reward(user_response)

        next_state = self.env.update_state(
            current_state=self.state,
            action=self.action_news,
            reward=reward,
            user_id=self.user_id,
        )

        self.memory.push(Episode(self.state, self.action_tensor, next_state, reward))
        optimize_model(self.memory, self.policy_net, self.target_net, self.optimizer)

        if self.iter_counter % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        self.reward_cum_sum += reward[0].item()

        print("Iteration:", self.iter_counter)
        self.iter_counter += 1

from collections import namedtuple
from os import getenv

# server
HOST = getenv('HOST', "localhost")
PORT = int(getenv('PORT', 8000))

# creates a struct with 4 four attributes
Episode = namedtuple('Episode',
                     ('state', 'action', 'next_state', 'reward'))

MEMORY_SIZE = 1000

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the AdamW optimizer

"""
Below, num_episodes is set to 600 if a GPU is available, otherwise 50 episodes are scheduled so 
training does not take too long. However, 50 episodes is insufficient for to observe good performance on cartpole. 
You should see the model constantly achieve 500 steps within 600 training episodes. 
Training RL agents can be a noisy process, so restarting training can produce better results 
if convergence is not observed.
"""

BATCH_SIZE = 1

""" https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
The discount, GAMMA, should be a constant between 0 and 1 that ensures the sum converges. 
A lower GAMMA makes rewards from the uncertain far future less important for our agent than the ones in the near future 
that it can be fairly confident about. It also encourages agents to collect reward closer in time than equivalent 
rewards that are temporally far away in the future.
"""
GAMMA = 0.3
EPS_START = 0
EPS_END = 0
EPS_DECAY = 500
"""
The target network is updated at every step with a soft update controlled by the hyperparameter TAU, 
which was previously defined.
"""
TAU = 1
LR = 1e-4

HIDDEN_SIZE = 64

# Model stuff
TARGET_UPDATE = 1

# Env stuff
# RANDOM_NEWS_RATE = 0.1
STATE_WINDOW = 10
NEWS_NUMBER = 10

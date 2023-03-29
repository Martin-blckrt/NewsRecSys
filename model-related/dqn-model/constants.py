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

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.3
EPS_END = 0.01
EPS_DECAY = 500
TAU = 0.005
LR = 1e-4

HIDDEN_SIZE = 64

# Model stuff
TARGET_UPDATE = 5

# Env stuff
RANDOM_NEWS_RATE = 0.1
STATE_WINDOW = 10
NEWS_NUMBER = 10

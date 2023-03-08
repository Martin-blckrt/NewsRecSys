from collections import namedtuple


# creates a struct with 4 four attributes
Transition = namedtuple('Transition',
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
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

INPUT_SIZE = 376  # state_size
OUTPUT_SIZE = 18  # action_space_size
HIDDEN_SIZE = 64

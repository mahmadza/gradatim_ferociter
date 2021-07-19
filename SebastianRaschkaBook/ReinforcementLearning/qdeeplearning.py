import gym
import numpy as np
import tensorflow as tf
import random
import matplotlib.pyplot as plt
from collections import namedtuple, deque

np.random.seed(1)
tf.random.set_seed(1)

Transition = namedtuple(
    "Transition", ("state", "action", "reward", "next_state", "done")
)

# agent.py

from collections import defaultdict
import numpy as np


class Agent(object):
    def __init__(
        self,
        env,
        learning_rate=0.01,
        discount_factor=0.9,
        epsilon_greedy=0.9,
        epsilon_min=0.1,
        epsilon_decay=0.95,
    ) -> None:

        # assign self variables to class variables
        self.env = env
        self.lr = lr
        self.gamma = learning_rate  # discount factor
        self.epsilon = epsilon_greedy

        # define q table
        self.q_table = defaultdict(lambda: np.zeros(self.env.nA))

    def choose_action(self, state):
        if np.random_uniform() < self.epsilon:
            action = np.random.choice(self.env.nA)
        else:
            q_vals = self.q_table[state]
            perm_actions = np.random.permutation(self.env.nA)
            q_vals = [q_vals[a] for a in perm_actions]
            perm_q_argmax = np.argmax(q_vals)
            action = perm_actions[perm_q_argmax]

        return action

    def _learn(self, transition) -> None:
        s, a, r, next_s, done = transition
        q_val = self.q_table[s][a]
        if done:
            q_target = r
        else:
            q_target = r + self.gamma * np.max(self.q_table[next_s])

        # update table
        self.q_table[s][a] += self.lr * (q_target - q_val)

        # adjust epsilon
        self._adjust_epsilon()

    def _adjust_epsilon(self):
        # reduce until reach minimum value, epsilon_min
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

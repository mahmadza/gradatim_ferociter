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


class DQNAgent:
    def __init__(
        self,
        env,
        discount_factor=0.95,
        epsilon_greedy=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.995,
        learning_rate=1e-3,
        max_memory_size=2000,
    ):
        self.env = env
        self.state_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.memory = deque(maxlen=max_memory_size)
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_decay = epsilon_decay
        self.lr = learning_rate
        self._build_nn_model()

    def build_nn_model(self, n_layers=3):
        self.model = tf.keras.Sequential()

        # hidden layers
        for n in range(n_layers - 1):
            self.model.add(tf.keras.layers.Dense(units=32, activation="relu"))
            self.model.add(tf.keras.layers.Dense(units=32, activation="relu"))

        # last layer
        self.model.add(tf.keras.layers.Dense(units=self.action_size))

        # build and compile model
        self.model.build(input_shape=(None, self.state_size))
        self.model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.lr))

    def remember(self, transition):
        self.memory.append(transition)

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)[0]
        return np.argmax(q_values)  # returns action

    def _learn(self, batch_samples):
        batch_states, batch_targets = [], []
        for transition in batch_samples:
            s, a, r, next_s, done = transition
            if done:
                target = r
            else:
                target = r + self.gamma * np.amax(self.model.predict(next_s)[0])

            target_all = self.model.predict(s)[0]
            target_all[a] = target
            batch_states.append(s.flatten())
            batch_targets.append(target_all)
            self._adjust_epsilon()
        return self.model.fit(
            x=np.array(batch_states), y=np.array(batch_targets), epochs=1, verbose=0
        )

    def _adjust_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def replay(self, batch_size):
        samples = random.sample(self.memory, batch_size)
        history = self._learn(samples)
        return history.history["loss"][0]

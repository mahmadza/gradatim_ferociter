# qlearning.py

from gridworld_env import GridWorldEnv
from agent import agent
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(1)

Transition = namedtuple(
    "Transition", ("state", "action", "reward", "next_state", "done")
)


def run_qlearning(agent, env, num_episodes=50):

    history = []

    for episode in range(num_episodes):
        state = env.reset()
        env.render(mode="human")
        final_reward, n_moves = 0.0, 0

        while True:
            action = agent.choose_action(state)
            next_s, reward, done, _ = env.step(action)
            agent._learn(Transition(state, action, reward, next_s, done))
            env.render(mode="human", done=done)
            state = next_s
            n_moves += 1
            if done:
                break
            final_reward = reward

        history.append((n_moves, final_reward))
        print("Episode %d: Reward %.1f #Moves %d" % (episode, final_reward, n_moves))

    return history

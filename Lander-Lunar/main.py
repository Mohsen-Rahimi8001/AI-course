import numpy as np
import random
import pickle
import time


class Qlearning:

    def __init__(self, env, number_of_iterations, rewrite_qtable=False) :
        self.env = env
        self.number_of_iterations = number_of_iterations
        self.alpha = 0.1
        self.gamma = 0.99
        
        if rewrite_qtable:
            self.initialize()
        else:
            self.q_values = self.load_qtable()
        
        self.action = [0, 1, 2, 3]
    
    @staticmethod
    def discretization(state):
        return (
            min(2, max(-2, int((state[0]) * 50))),
            min(2, max(-2, int((state[1]) * 10))),
            min(2, max(-2, int((state[2]) * 10))),
            min(2, max(-2, int((state[3]) * 10))),
            min(2, max(-2, int((state[4]) * 10))),
            min(2, max(-2, int((state[5]) * 10))),
            int(state[6]),
            int(state[7])
        )

    def initialize(self):
        self.q_values = dict()
        self.save_qtable()

    def load_qtable(self):
        with open("q_table.pkl", "rb") as f:
            return pickle.load(f)
    
    def save_qtable(self):
        with open("q_table.pkl", "wb") as f:
            pickle.dump(self.q_values, f)

    def get_q_value(self , state , action):
        try:
            return self.q_values[(state , action)]
        except KeyError:
            return 0

    def max_value(self, state):
        mx = -100000000
        for act in self.action:
            if (new_val:=self.get_q_value(state , act)) > mx:
                mx = new_val
        return mx

    def max_action(self, state):
        mx = self.max_value(state)
        for act in self.action: 
            if self.get_q_value(state , act) == mx:
                return act
    
    def update(self, state, action, next_state, reward, terminated, truncated):
        if terminated or truncated:
            self.q_values[(state , action)] = self.get_q_value(state, action) + self.alpha * (reward - self.get_q_value(state, action))
        else:
            self.q_values[(state, action)] = self.get_q_value(state , action) + self.alpha * (reward + (self.gamma * self.max_value(next_state)) - self.get_q_value(state, action))

    def train(self):
        next_state, _ = self.env.reset(seed=int(time.time()) % 550 + 50)
        total_reward = 0
        for i in range(self.number_of_iterations):
            while True:
                current_state = self.discretization(next_state)
                action = self.max_action(current_state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                total_reward += reward
                next_statetmp = self.discretization(next_state)
                self.update(current_state, action, next_statetmp, reward, terminated, truncated)
                self.env.render()

                if terminated or truncated:
                    print(f"episode: {i}, total reward: {total_reward}")
                    total_reward = 0
                    next_state, _ = self.env.reset()
                    break
                
            if i + 1 == self.number_of_iterations:
                self.save_qtable()

if __name__ == "__main__":
    import gymnasium as gym
    import sys
    
    if sys.argv[1] == "train":
        env = gym.make('LunarLander-v2')
        agent = Qlearning(number_of_iterations=1500, env=env, rewrite_qtable=False)
        agent.train()
        env.close()
    
    elif sys.argv[1] == "test":
        env = gym.make('LunarLander-v2', render_mode="human")
        agent = Qlearning(number_of_iterations=3, env=env)
        agent.train()
        
        env.close()
"""A simple q-learning experiment
by Felix Patzelt 2024
"""
from typing import List
import numpy as np

class q_learner():
    """Naive q-learning agent
    
    Implementing reward table "q[state,action]" as a key-value map
    """
    def __init__(
        self,
        q_init:float = 1, # initial q > 0 incentivises exploration
        learning_rate:float = .9, # "alpha"
        discount_factor:float = .1, # "gamma"
        p_explore:float = 0.01,
        rng:np.random.Generator = np.random.default_rng() # allows to control randomness
    ):
        self.q:dict = {} # the reward "table"
        self.q_init = q_init
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.p_explore = p_explore
        self.rng = rng
        self.verbose = False
    
    def get_q_s(self,state:str, actions:list):
        q_s = self.q.get(state, {})
        q_s = {a: self.q_init for a in actions} | q_s # fill q for missing actions
        return q_s
    
    def choose_action(self, state:str, actions: List[str]):
        "Explore or choose action maximising q. returns action & q"
        q_s = self.get_q_s(state, actions)
        if self.p_explore > self.rng.uniform():
            if self.verbose: print("explore")
            j = self.rng.integers(0, len(actions))
            action = actions[j]
        else:
            if self.verbose: print("exploit")
            if self.verbose: print(q_s)
            action = max(q_s, key=q_s.get)
        return action, q_s[action]
    
    def learn(self, state:str, action:str, action_q:float, new_state:str, new_state_q:float, new_actions:List[str]):
        max_new_q = max(self.get_q_s(new_state, new_actions).values())
        if self.verbose: print("q_sa", action_q)
        new_action_q = (
            (1 - self.learning_rate) * action_q
            + self.learning_rate * (new_state_q + self.discount_factor * max_new_q)
        )
        if state in self.q:
            self.q[state].update({action: new_action_q})
        else:
            self.q[state] = {action: new_action_q}
        if self.verbose: print(f"new q", self.q)

"""A super simple test scenario"""
from typing import List

class find_the_keys():
    """A little test world to get going with learning a state space
    you left the house and realise you don't have your keys. where are they?
    this is the most naive an inefficient text adventure on purpose.
    
    When collecting the reward it makes sense to call the reset() method
    which goes back to the beginning. It is not strictly necessary though.
    """
    def __init__(self):
        #world = [('description', reward, [nested_world])]
        self.world = (
            'look around', 0, [
                ('go left', 0, [
                    ('climb tree', 0, []),
                    ('search floor', 0, [
                        ('lift stone', 0,[]),
                        ('lift leaf', 0,[])
                    ])
                ]),
                ('go straight', 0, [
                    ('enter house', 0, [
                        ('check cupboard', 1, []),
                        ('check wardrobe', 0, [])
                    ])
                ]),
                ('go right', 0, [
                    ('check bike', 0, []), # bike is locked
                    ('check mailbox', 0, [
                        ('open first letter', 0, []),
                        ('open second letter', 0, []),
                        ('open third letter', 0, []),
                    ])
                ])
            ]
        )
        self.reset()
        
        
    def _get_state(self):
        state = self.world
        description = state[0]
        reward = state[1]
        actions = state[2]
        # go through all previous states to current one
        for a in self.previous_actions:
            description, reward, actions = actions[a]
        return description, reward, actions
    
    def _set_state(self, previous_actions:List[int]):
        self.previous_actions = previous_actions
        self.description, self.reward, self.actions = self._get_state()
        
    def reset(self):
        self._set_state([])
    
    def get_description(self):
        return self.description
    
    def get_reward(self):
        return self.reward
    
    def _get_actions_and_rewards(self):
        return [(a[0], a[1]) for a in self.actions] + [('go back', 0)]
    
    def get_actions(self):
        return [a[0] for a in self.actions] + ['go back']

    def do(self, action:str):
        if action == 'go back':
            self._set_state(self.previous_actions[:-1])
            return "done"
        else:
            for i, a in enumerate(self._get_actions_and_rewards()):
                if a[0] == action:
                    self._set_state(self.previous_actions + [i])
                    return "done"
        return "impossible"
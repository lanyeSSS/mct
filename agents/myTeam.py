from template import Agent
import random, time
from copy import deepcopy
from collections import deque

from Splendor.splendor_model import SplendorGameRule as GameRule
from Splendor.splendor_utils import *

THINKTIME = 0.95
GAMMA = 0.9
NUM_PLAYERS = 2
EPSILON = 0.6

class myAgent(Agent):
    def __init__(self, _id):
        super().__init__(_id)
        self.game_rule = GameRule(NUM_PLAYERS)

    def GetActions(self, state):
        return self.game_rule.getLegalActions(state, self.id)

    def DoAction(self, state, action):
        state = self.game_rule.generateSuccessor(state, action, self.id)

    def GameEnd(self, state):
        score = state.agents[self.id].score
        return score >= 15

    def GetScore(self, state):
        return state.agents[self.id].score

    def ActionInList(self, action, action_list):
        q_action = ActionToString(self.id, action)
        return (q_action in action_list)

    def TransformState(self, state, _id):
        t_state = state.__str__()
        return t_state

    def SelectAction(self, actions, game_state):
        start_time = time.time()
        # MCT
        q_sa = dict()
        n_sa = dict()
        expanded_action_s = dict()
        t_root_state = 'r'

    def FullyExpanded(self, t_state, actions):
        if t_state in expanded_action_s:
            available_actions = []
            for action in actions:
                if not self.ActionInList(action, expanded_action_s[t_state]):
                    available_actions.append(action)
            return available_actions
        else:
            return actions

    def GetBestAction(self, t_state, actions):
        max_value = -float('inf')
        best_action = random.choice(actions)
        for action in actions:
            t_sa = t_state + ActionToString(self.id, action)
            if (t_sa in q_sa) and (q_sa[t_sa] > max_value):
                max_value = q_sa[t_sa]
                best_action = action
        return best_action

    while time.time() - start_time < THINKTIME:
    count += 1
    state = deepcopy(game_state)
    new_actions = actions
    t_cur_state = t_root_state
    queue = deque([])
    reward = 0
    
    # Select
    while len(FullyExpanded(t_cur_state, new_actions)) == 0 and not self.GameEnd(state):
        if time.time() - start_time >= THINKTIME:
            print("MCT:", count)
            return GetBestAction(t_root_state, actions)
        t_cur_state = self.TransformState(state, self.id)
        if random.uniform(0, 1) < 1 - EPSILON:
            cur_action = GetBestAction(t_cur_state, new_actions)
        else:
            cur_action = random.choice(new_actions)
        
        queue.append((t_cur_state, cur_action))
        next_state = deepcopy(state)
        self.DoAction(next_state, cur_action)
        new_actions = self.GetActions(next_state)
        state = next_state

    # Expand
    t_cur_state = self.TransformState(state, self.id)
    available_actions = FullyExpanded(t_cur_state, new_actions)
    if len(available_actions) == 0:
        continue
    else:
        action = random.choice(available_actions)
        if t_cur_state in expanded_action_s:
            expanded_action_s[t_cur_state].append(ActionToString(self.id, action))
        else:
            expanded_action_s[t_cur_state] = [ActionToString(self.id, action)]
        
        queue.append((t_cur_state, action))
        next_state = deepcopy(state)
        self.DoAction(next_state, action)
        new_actions = self.GetActions(next_state)
        state = next_state

    # Simulation
    length = 0
    while not self.GameEnd(state):
        length += 1
        if time.time() - start_time >= THINKTIME:
            print("MCT:", count)
            return GetBestAction(t_root_state, actions)
        cur_action = random.choice(new_actions)
        next_state = deepcopy(state)
        self.DoAction(next_state, cur_action)
        new_actions = self.GetActions(next_state)
        state = next_state
    
    reward = self.GetScore(state)

    # Backpropagate
    cur_value = reward * (GAMMA ** length)
    while len(queue) and time.time() < THINKTIME:
        t_state, cur_action = queue.pop()
        t_sa = t_state + ActionToString(self.id, cur_action)
        if t_sa in q_sa:
            n_sa[t_sa] += 1
            q_sa[t_sa] = q_sa[t_sa] + (cur_value - q_sa[t_sa]) / n_sa[t_sa]
        else:
            q_sa[t_sa] = cur_value
            n_sa[t_sa] = 1
        cur_value *= GAMMA

print("MCT:", count)
return GetBestAction(t_root_state, actions)




from gym import spaces
import numpy as np
import random
import pandas as pd
from itertools import groupby
from itertools import product

class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix
        self.reset()

    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        
        # check for rows
        if curr_state[0] + curr_state[1] + curr_state[2] == 15:
            return True
        elif curr_state[3] + curr_state[4] + curr_state[5] == 15:
            return True
        elif curr_state[6] + curr_state[7] + curr_state[8] == 15:
            return True

        #check for cols
        if curr_state[0] + curr_state[3] + curr_state[6] == 15:
            return True
        elif curr_state[1] + curr_state[4] + curr_state[7] == 15:
            return True
        elif curr_state[2] + curr_state[5] + curr_state[8] == 15:
            return True

        #checks for diagonals
        if curr_state[0] + curr_state[4] + curr_state[8] == 15:
            return True
        elif curr_state[2] + curr_state[4] + curr_state[6] == 15:
            return True

        return False

    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if pd.isnull(val)]

    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not pd.isnull(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)

    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        
        return (agent_actions, env_actions)

    def stepsssss(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""

        # new_state = self.state_transition(curr_state, curr_action)
        # reward = self.reward(curr_state, curr_action)
        # isGameEnded = self.is_terminal(new_state)[0]
        # curr_state = new_state
        # if isGameEnded:
        #     return new_state,reward,isGameEnded

        env_action = random.choice(list(env.action_space(curr_state)[1]))
        new_state = self.state_transition(curr_state, env_action)
        isGameEnded = self.is_terminal(new_state)[0]
        if isGameEnded:
            return new_state,-10,True

        # return the new state (after env move), reward that agent earned and is game ended after env move
        return new_state,reward,isGameEnded

    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        cell_position = curr_action[0]
        cell_value = curr_action[1]

        new_state = curr_state
        new_state[cell_position] = cell_value
        return new_state

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        return False, 'Resume'


    def reward(self, curr_state, curr_action):
        board_state = self.is_terminal(new_state)
        
        if board_state[0] == True:
            if board_state[1] == 'Win':
                return 10 #player wins
            elif board_state[1] == 'Tie':
                return 0 #draw
        else: #resume state
            return -1

    def reset(self):
        return self.state
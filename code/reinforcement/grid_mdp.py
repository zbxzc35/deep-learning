'''
Created on Mar 13, 2016

@author: trucvietle
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter
from textwrap import dedent
from itertools import *
import numpy as np

def parse():
    '''
    Parse command/terminal line.
    '''
    class CustomFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
        pass
    parser = ArgumentParser(formatter_class=CustomFormatter,
                            description=dedent('To be filled.'),
                            epilog=dedent('To be filled.'))
    parser.add_argument('-r', '--nrow', type=int, default=3, help='Number of rows')
    parser.add_argument('-c', '--ncol', type=int, default=4, help='Number of columns')
    return vars(parser.parse_args())
    
def build_environment(nrow=3, ncol=4):
    ## Set the initial rewards
    rewards = np.zeros(shape=(nrow, ncol))
    ## Coordinates of the 'wall'
    wall_row = int(nrow / 2)
    wall_col = int(ncol / 2) - 1
    ## Set the reward values
    rewards[wall_row, wall_col] = None
    rewards[0, ncol-1] = 1 # the goal
    rewards[1, ncol-1] = -1 # the trap
    
    ## Set the initial values
    values = rewards
    ## The set of states are the grid cells
    states = product(range(nrow), range(ncol))
    states = list(states) # convert iterator to list
#     print rewards[max(states)]
#     for state in states:
#         print state
    ## Create the transition probabilities
    transition = {}
    transition['N'] = [0.8, 0, 0.1, 0.1] # north, south, east, west
    transition['S'] = [0, 0.8, 0.1, 0.1]
    transition['E'] = [0.1, 0.1, 0.8, 0]
    transition['W'] = [0.1, 0.1, 0, 0.8]
    
    ## The value of an action
    action_values = {}
    action_values['N'] = [-1, 0] # x, y
    action_values['S'] = [1, 0]
    action_values['E'] = [0, 1]
    action_values['W'] = [0, -1]
    
    return rewards, values, states, transition
    
def act(action_values, action, states, state, rewards):
    '''
    Moves the agent through the states based on action taken.
    '''
    action_value = action_values[action]
    new_state = state
    goal_row = 0
    goal_col = max(states)[1]
    trap_row = 1
    trap_col = max(states)[1]
    if (state[0] == goal_row and state[1] == goal_col) or (state[0] == trap_row and state[1] == trap_col):
        ## Reached the goal or the trap
        return state
    new_row = state[0] + action_value[0]
    new_col = state[1] + action_value[1]
    
    ## Constrained by the edge of the grid
    new_state[0] = min(max(states)[0], max(0, new_row))
    new_state[1] = min(max(states)[1], max(0, new_col))
    
    if rewards[new_state] is None:
        new_state = state
    
    return new_state

if __name__ == '__main__':
    params = parse()
    nrow = params['nrow']
    ncol = params['ncol']
    build_environment(nrow, ncol)
    
import numpy as np
import scipy

TEAM_NAME = "mikeys_ducks"
MEMBERS = ["syc5pg", "jjp5nw", "ar9fh", "jn3qf"]
mikeys_ducks_info = {'utility': 1000000}
'''
{
    "team-code": "eef8976e",
    "game": "phase_1",
    "pulls-left": 99999,
    "last-cost": 0.75,
    "last-payoff": 20.7,
    "last-metadata": 00110101
}
'''


def check_key(state, key):
    if key not in state or state[key] == None:
        return False
    return True

#should update info with a list of top 10 machines to buy maybe
def phase1(state):
    mikeys_ducks_info['auctions'] = []
    pass
###

def phase2a(state):
    return {
    "team-code": "eef8976e",
    "game": "phase_2_a",
    "auctions": mikeys_ducks_info['auctions']
    }
###

def phase2b(state):
    num_buyers = len(state['auction-lists'][state['auction-number']])
    utility = mikeys_ducks_info['utility']
    # utility/num_auctions * payoff_factor * num_buyers_factor

    pass

def get_move(state):
    if(state["game"] == "phase_1"):
        return phase1(state)
    elif(state["game"] == "phase_2_a"):
        return phase2a(state)
    elif(state["game"] == "phase_2_b"):
        return phase2b(state)
    else:
        raise Exception("Game not specified")

def main():
    pass
###

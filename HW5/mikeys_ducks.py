import numpy as np
from random import randint, uniform
from scipy.stats import beta as beta_mod
from time import time

TEAM_NAME = "mikeys_ducks"
MEMBERS = ["syc5pg", "jjp5nw", "ar9fh", "jn3qf"]
mikeys_ducks_info = {'utility': 1000000, 'machines-done': set()}
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

def get_best_profit_index():
    best_ind = 0
    while best_ind in mikeys_ducks_info['machines-done']:
        best_ind += 1
    best_prof= mikeys_ducks_info['alph-beta-scal'][best_ind][0] - mikeys_ducks_info['costs'][best_ind]

    for i in range(100):
        if i in mikeys_ducks_info['machines-done']:
            continue
        new_prof = mikeys_ducks_info['alph-beta-scal'][i][0] - mikeys_ducks_info['costs'][i]
        if new_prof > best_prof:
            best_ind = i
            best_prof= new_prof
    return best_prof, best_ind

def phase1(state): 
    """
    if state['pulls-left'] % 100 == 0:
        print(state['pulls-left'])
    """

    if state['pulls-left'] == 9000:
        mikeys_ducks_info['alph-beta-scal'] = []
        for i in range(100):
            alph, beta, _, scal = beta_mod.fit(mikeys_ducks_info['payoffs'][i])
            mikeys_ducks_info['alph-beta-scal'].append(((scal*alph)/(alph+beta), alph, beta, scal, i))

    if state['pulls-left'] == 10000:
        mikeys_ducks_info['costs'] = [0 for i in range(100)]
        mikeys_ducks_info['metadata'] = ['00000000' for i in range(100)]
        mikeys_ducks_info['payoffs'] = [[] for i in range(100)]

    if check_key(state, 'last-cost'):
        last_pull = mikeys_ducks_info['last-pull']
        mikeys_ducks_info['utility'] += (state['last-payoff'] - state['last-cost'])
        mikeys_ducks_info['costs'][last_pull] = state['last-cost']
        mikeys_ducks_info['metadata'][last_pull] = state['last-metadata']
        mikeys_ducks_info['payoffs'][last_pull].append(state['last-payoff'])
        if len(mikeys_ducks_info['payoffs'][last_pull]) >=  1000:
            mikeys_ducks_info['machines-done'].add(last_pull)
        if check_key(mikeys_ducks_info, 'alph-beta-scal') and state['pulls-left'] % 10 == 0:
            alph, beta, _, scal = beta_mod.fit(mikeys_ducks_info['payoffs'][last_pull])
            mikeys_ducks_info['alph-beta-scal'][last_pull] = (scal*alph/(alph+beta), alph, beta, scal, last_pull)


    move = {}
    move['team-code'] = state['team-code']
    move['game'] = 'phase_1'
    if state['pulls-left'] > 9000:
        move['pull'] = int((10000 - state['pulls-left'])/10)
    else:
        best_prof, best_ind = get_best_profit_index()
        move['pull'] = best_ind

    mikeys_ducks_info['last-pull'] = move['pull']
    return move
        
        
###

def phase2a(state):
    pass
###

def phase2b(state):
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


if __name__ == "__main__":
    machine_tups = []
    for i in range(100):
        # alph, beta, scal, cost
        machine_tups.append((randint(1, 10), randint(1, 10), uniform(0.1, 20), uniform(0.1, 20)))

    state = {
        "team-code": "eef8976e",
        "game": "phase_1",
        "last-cost": None,
        "last-payoff": None,
        "last-metadata": '00001111'
    }

    time_start = time()
    for i in range(10000):
        state['pulls-left'] = 10000 - i
        pull = get_move(state)['pull']
        alph, beta, scal, cost = machine_tups[pull]
        state['last-cost'] = cost
        state['last-payoff'] = np.random.beta(alph, beta) * scal

    absi_sorted = sorted(mikeys_ducks_info['alph-beta-scal'], key=lambda x: len(mikeys_ducks_info['payoffs'][x[4]]))
    for i in range(100):
        ind = absi_sorted[i][4]
        act_prof = machine_tups[ind][2] * (machine_tups[ind][0]/(machine_tups[ind][0] + machine_tups[ind][1])) - machine_tups[ind][3]
        """
        print(ind)
        print("%2d %2d %5.2f %5.2f = %5.2f" % (machine_tups[ind][0], machine_tups[ind][1], machine_tups[ind][2], machine_tups[ind][3], act_prof))
        print("%2d %2d %5.2f %5.2f = %5.2f" % (int(round(absi_sorted[i][1])), int(round(absi_sorted[i][2])), absi_sorted[i][3], mikeys_ducks_info['costs'][ind], absi_sorted[i][0] - mikeys_ducks_info['costs'][ind]))
        print(len(mikeys_ducks_info['payoffs'][ind]))
        print("")
        """
    print("Total utility:", mikeys_ducks_info['utility'])
    print(time() - time_start)
        

###

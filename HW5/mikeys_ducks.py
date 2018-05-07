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
	return key in state and state[key] != None
	# if key not in state or state[key] == None:
	# 	return False
	# return True

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
	elif state['pulls-left'] == 10000:
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

	if state['pulls-left'] == 1:
		mikeys_ducks_info['machines-done'].add(move['pull'])
		mikeys_ducks_info['auctions'] = sorted(list(mikeys_ducks_info['machines-done']),
											   key = lambda x: -1*(mikeys_ducks_info['alph-beta-scal'][x][0] - mikeys_ducks_info['costs'][x]))
	return move
###

def phase2a(state):
	return {
	"team-code": state["team-code"],
	"game": "phase_2_a",
	"auctions": mikeys_ducks_info['auctions']
	}
###


'''
{
"team-code": "eef8976e",
"game": "phase_2_b",
"auction-number": 20,
"your-slots": [],
"auction-lists": [
["eef8976e", ...]
...
]
}
'''

def phase2b(state):
	num_buyers = len(state['auction-lists'][state['auction-number']])
	utility = mikeys_ducks_info['utility']
	# utility/num_auctions * payoff_factor * num_buyers_factor
	
	current_slot_machine = state['auction-number']
	expected_value = mikeys_ducks_info['alph-beta-scal'][current_slot_machine][0]
	cost = mikeys_ducks_info['costs'][current_slot_machine]

	expected_payoff = expected_value - cost

	percentage = 1.0
	number_of_plays = 10000

	our_bid = percentage * number_of_plays * expected_payoff if (current_slot_machine in mikeys_ducks_info['auctions']) else 0

	return {
		"team-code": state["team-code"],
		"game": "phase_2_b",
		"bid": our_bid
	}

###

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
		# Sets up machines with the following
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
		# Prints the following
		# Machine number
		# Actual    alpha beta scale cost = actual expected payoff
		# Predicted alpha beta scale cost = predicted expected payoff
		# Number of times pulled
		print(ind)
		print("%2d %2d %5.2f %5.2f = %5.2f" % (machine_tups[ind][0], machine_tups[ind][1], machine_tups[ind][2], machine_tups[ind][3], act_prof))
		print("%2d %2d %5.2f %5.2f = %5.2f" % (int(round(absi_sorted[i][1])), int(round(absi_sorted[i][2])), absi_sorted[i][3], mikeys_ducks_info['costs'][ind], absi_sorted[i][0] - mikeys_ducks_info['costs'][ind]))
		print(len(mikeys_ducks_info['payoffs'][ind]))
		print("")

	print("Total utility:", mikeys_ducks_info['utility'])
	print(mikeys_ducks_info['auctions'])
	print(time() - time_start)



	#############################################
	# Phase 2b Test
	phase2b_state = {
	"team-code": "eef8976e",
	"game": "phase_2_b",
	"auction-number": 0,
	"your-slots": [],
	"auction-lists": [['some-team-code'] for i in range(100)]
	}

	phase2b_test = get_move(phase2b_state)

	print("0: " + str(phase2b_test))

	for slot_machine in mikeys_ducks_info['auctions']:
		phase2b_state = {
		"team-code": "eef8976e",
		"game": "phase_2_b",
		"auction-number": slot_machine,
		"your-slots": [],
		"auction-lists": [['some-team-code'] for i in range(100)]
		}

		phase2b_test = get_move(phase2b_state)

		print(str(slot_machine) + ": " + str(phase2b_test))
	#
	

###

# 

TEAM_NAME = "mikeys_ducks"
MEMBERS = ["syc5pg", "jjp5nw", "ar9fh", "jn3qf"]

mikeys_ducks_info = {}

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

def phase1(state): 
    pass
###

def phase2(state):
    pass
###

def get_move(state):
    if(state["game"] == "phase_1"):
        return phase1(state)
    elif(state["game"] == "phase_2_a"):
        # return phase2(state, 
        # put what is needed for phase2 here
        pass
    elif(state["game"] == "phase_2_b"):
        pass
    else:
        pass
    #

###

def main():
    pass
###






#################################
if __name__ == "__main__":      #
    main()                      #
#################################


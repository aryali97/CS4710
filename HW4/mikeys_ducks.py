TEAM_NAME = "mikeys_ducks" #Pick a team name
MEMBERS = ["syc5pg", "jjp5nw", "ar9fh", "jn3qf"] #Include a list of your members’ UVA IDs
mikeys_ducks_info = {}


'''
# sample state format: 

state = {
"team-code": "eef8976e",
"game": "sym",
"opponent-name": "mighty-ducks",
"prev-repetitions": 10, #Might be None if first game ever, or other number
"last-opponent-play": 1, #0 or 1 depending on strategy played
"last-outcome": 4, #Might be None if first game, or whatever outcome of play is
"prospects": [
[4,5],
[3,2]
]
}

'''

def get_greatest_index(lst, obj):
    for i in range(len(lst)-1, -1, -1):
        if lst[i] == obj:
            return i
    return -1

def get_move(state):
    move = {}
    move['team-code'] = state['team-code']
    prosps = state['prospects'][0] + state['prospects'][1]
    argmin = get_greatest_index(prosps, min(prosps))
    argmax = get_greatest_index(prosps, max(prosps))
    val = 1
    look_back_num =2 
    
    if state['prev-repetitions'] is None:
        mikeys_ducks_info.setdefault('opponent-plays',{}).setdefault(state['opponent-name'],[])
        val = (int)(argmin not in [2,3])
    else:
        mikeys_ducks_info['opponent-plays'][state['opponent-name']].append(state['last-opponent-play'])
        opp_plays = mikeys_ducks_info['opponent-plays'][state['opponent-name']]
        safe_play = (int)(argmin not in [2,3])
        tempt_play = (int)(argmax in [2,3])
        if tempt_play == safe_play:
            val = safe_play
        elif len(opp_plays) >= look_back_num:
            same_play = True
            for i in range(len(opp_plays) - (look_back_num-1), len(opp_plays)):
               if opp_plays[i] != opp_plays[i-1]:
                   same_play = False
                   break
            if not same_play:
                val = safe_play
            else:
                prop_abs = 0.5
                opp_pred_play = opp_plays[len(opp_plays) - 1]
                prosp_1 = 2+opp_pred_play
                prosp_0 = opp_pred_play
                abs_diff = prosps[prosp_1] - prosps[prosp_0]
                flip_if_1 = prosp_1 if prosp_1 in [0, 3] else ((1 - (prosp_1 - 1)) + 1)
                flip_if_0 = prosp_0 if prosp_0 in [0, 3] else ((1 - (prosp_0 - 1)) + 1)
                pre_diff= (prosps[prosp_1]-prosps[flip_if_1]) - \
                          (prosps[prosp_0]-prosps[flip_if_0])
                val = (int)((abs_diff*prop_abs + pre_diff*(1-prop_abs)) > 0)
        else:
            val = safe_play
    move['move'] = val
    return move

"""
if __name__ == "__main__":
    state = {
        "team-code": "eef8976e",
        "game": "sym",
        "opponent-name": "mighty-duck",
        "prev-repetitions": None, #Might be None if first game ever, or other number
        "last-opponent-play": None, #0 or 1 depending on strategy played
        "last-outcome": None, #Might be None if first game, or whatever outcome of play is
        "prospects": [
        [10,9],
        [120,0]
        ]
    }
    our_score = 0
    opp_score = 0
    for i in range(10):
        our_move = get_move(state)['move']
        prosps = state['prospects'][0] + state['prospects'][1]
        argmin = get_greatest_index(prosps, min(prosps))
        argmax = get_greatest_index(prosps, max(prosps))
        opp_move = (int)(argmax in [2,3])
        our_score += prosps[opp_move+2*our_move]
        opp_score += prosps[our_move+2*opp_move]
        print("Round", i)
        print("Our play", our_move)
        print("Opp play", opp_move)
        print("Payoff (%d, %d)" % (prosps[opp_move+2*our_move], prosps[our_move+2*opp_move]))
        print("Our score", our_score)
        print("Opp score", opp_score)
        print("")
        state['prev-repetitions'] = i
        state['last-opponent-play'] = opp_move
        state['last-outcome'] = prosps[opp_move+2*our_move]
        

###
"""

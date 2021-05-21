import wsls
import json
import numpy as np 

"""
computes the likelihood of a win stay lose shift model for a participant
"""

def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(variables, rewards, options):
    p_stay = variables[0]
    p_shift = variables[1]

    if p_stay>1: return 2389238330984903
    if p_stay<0: return 2888888392833392
    if p_shift>1: return 28392393332839
    if p_shift<0: return 28392833333928

    prev_option = options[0]
    prev_reward = options[1]
    probs = []

    for i in range(len(options)-1):
        prob = wsls.participantCalc(p_stay,p_shift,prev_option,prev_reward,options[i])
        probs.append(prob)
        prev_option = options[i]
        prev_reward = rewards[i]

    return np.sum([-np.log(x) for x in probs])
import vse
import json
import numpy as np 


#w = 1
#a = 0.4
#c = 3

"""
computes the log-likelihood for the vse model, if the parameters are out of range, it returns large likelihoods
this forces the optimisation function away from boundaries
"""

#filename = 'options_trial/clean_05-03-21-154538.json'

def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(variables, rewards, options):
    delta = variables[0]
    alpha = variables[1]
    phi = variables[2]
    c = variables[3]
    likelihoods = [0.25]
    if delta >1:return 1000000
    elif delta<0:return 2200000
    elif alpha>1: return 100000
    elif alpha<0: return 2999999
    elif c>5: return 2999999
    elif c<0: return 29999999
    exploit = [1]*4
    explore = [1]*4
    v = [0]*4
    prob = [0.25]*4
    for i in range(len(options)-1):
        v,exploit,explore,prob = vse.participantCalc(delta,alpha,phi, v,explore,exploit, prob, c,rewards[i],options[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])
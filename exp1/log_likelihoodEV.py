import EVPU
import json
import numpy as np 


#w = 1
#a = 0.4
#c = 3

#filename = 'options_trial/clean_05-03-21-154538.json'
"""
EV-PU MODEL
Computes the log likelihood of the EV-PU model given the model parameters, this script is used in the optimisation stage 
and is used to test all parameters using Nelder Mead.
"""
def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihoodEV(variables, rewards, options):
    w = variables[0]
    a= variables[1]
    c = variables[2]
    likelihoods = [0.25]
    if w<0: return 10000000
    elif w>5: return 100000
    if a>1: return 100000
    elif a<0: return 100000
    elif c>5: return 100000
    elif c<-5: return 1000000 #avoiding params going out of range
    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    t = 0
    for i in range(len(options)-1):
        u, Ev, prob,t = EVPU.participantCalc(w,u,a,Ev,prob,c,rewards[i],options[i],t)
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])
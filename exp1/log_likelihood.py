import pvl 
import json
import numpy as np 


#w = 1
#a = 0.4
#c = 3

#filename = 'options_trial/clean_05-03-21-154538.json'

"""
PVL MODEL
Using participant data from the getInfo function, this script computes the log likelihood of the model given a set of parameters
"""

def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(variables, rewards, options):
    w = variables[0]
    a= variables[1]
    c = variables[2]
    likelihoods = [0.25]
    if w<0: return 10000000
    elif w>5: return 100000
    if a>1: return 100000
    elif a<0: return 100000
    elif c>5: return 100000
    elif c<0: return 1000000 #avoiding params going out of range
    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    for i in range(len(options)-1):
        u, Ev, prob = pvl.participantCalc(w,u,a,Ev,prob,c,rewards[i],options[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])


#json_file = open(filename, 'r')
#rewards, options = getInfo(json_file)
#likelihood = computeLikelihood(rewards, options, w, a, c)
#print(likelihood)



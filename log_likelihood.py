import pvl 
import json
import numpy as np 

#w = 1
#a = 0.4
#c = 3

#filename = 'options_trial/clean_05-03-21-154538.json'

def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(filename, w, a, c):
    json_file = open(filename, 'r')
    rewards, options = getInfo(json_file)
    likelihoods = [0.25]
    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    for i in range(len(options)-1):
        u, Ev, prob = pvl.participantCalc(w,u,a,Ev,prob,c,rewards[i],options[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])



#likelihood = computeLikelihood(filename, w, a, c)




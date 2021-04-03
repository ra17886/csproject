import pvl 
import json
import numpy as np 

w = 1
a = 0.4
c = 3

filename = 'options_trial/clean_05-03-21-154538.json'
json_file = open(filename, 'r')



def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    return rewards, options

def computeLikelihood(json_file, w, a, c):
    rewards, options = getInfo(json_file)
    print(options)
    likelihoods = [0.25]
    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    for i in range(len(options)-1):
        u, Ev, prob = pvl.participantCalc(w,u,a,Ev,prob,c,rewards[i],options[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])


    #then get the second option and add corresponding prob to likelihood array

likelihood = computeLikelihood(json_file, w, a, c)




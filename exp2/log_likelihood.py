import pvl 
import json
import numpy as np 
import evpu
import vse
import wsls

"""
computes log likelihood for each participant, iff the paramter is out of range, returns a high log likelihood
"""

def getInfo(json_file):
    data = json.load(json_file)
    rewards = [int(x) for x in data['rewards']]
    options = [int(x) for x in data['options']]
    penalties = [int(x) for x in data['penalties']]
    return rewards, options, penalties

def computeLikelihoodPVL(variables, rewards, options,penalties):
    w = variables[0]
    a= variables[1]
    c = variables[2]
    shape = variables[3]
    likelihoods = [0.25]

    if w<0: return 10000000
    elif w>5: return 100000
    if a>1: return 100000
    elif a<0: return 100000
    if c>5: return 100000
    elif c<0: return 1000000 
    if shape<0: return 10000000
    elif shape>1: return 1000000 #avoiding params going out of range

    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    for i in range(len(options)-1):
        u, Ev, prob = pvl.participantCalc(w,u,a,Ev,prob,c,shape,rewards[i],options[i],penalties[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])

def computeLikelihoodEVPU(variables, rewards, options,penalties):
    w = variables[0]
    a= variables[1]
    c = variables[2]
    shape = variables[3]
    likelihoods = [0.25]

    if w<0: return 10000000
    elif w>5: return 100000
    if a>1: return 100000
    elif a<0: return 100000
    elif c>5: return 100000
    elif c<-5: return 1000000
    elif shape <0: return 1000000
    elif shape>5: return 1000000 #avoiding params going out of range

    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    t = 0
    for i in range(len(options)-1):
        u, Ev, prob,t = evpu.participantCalc(w,u,a,Ev,prob,c,shape,rewards[i],options[i],penalties[i], t)
        #print(prob[options[i+1]])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])

def computeLikelihoodVSE(variables, rewards, options,penalties):
    delta = variables[0]
    alpha = variables[1]
    phi = variables[2]
    c = variables[3]
    theta = variables[4]
    likelihoods = [0.25]

    if delta >1:return 1000000
    elif delta<0:return 2200000
    elif alpha>1: return 100000
    elif alpha<0: return 2999999
    elif c>5: return 2999999
    elif c<0: return 29999999
    elif theta>1: return 77777777
    elif theta<0: return 292999999

    exploit = [1]*4
    explore = [1]*4
    v = [0]*4
    prob = [0.25]*4

    for i in range(len(options)-1):
        v,exploit,explore,prob = vse.participantCalc(delta,alpha,phi,theta, v,explore,exploit, prob, c,rewards[i],options[i],penalties[i])
        likelihoods.append(prob[options[i+1]])
    return np.sum([-np.log(x) for x in likelihoods])

def computeLikelihoodWSLS(variables, rewards, options):
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

"""
w= 4.7
a = 0.8
c = 4
shape = 0.01

delta = 0.99
alpha = 0.99
phi = 0
theta = 0.99

filename = 'trial/clean_24-04-21-145858.json'

json_file = open(filename, 'r')
rewards, options, penalties = getInfo(json_file)
PVL_likelihood = computeLikelihoodPVL([w,a,c,shape],rewards, options,penalties)
EV_likelihood = computeLikelihoodEV([w,a,c,shape],rewards,options,penalties)
VSE_likelihood = computeLikelihoodVSE([delta,alpha,phi,c,theta], rewards, options,penalties)
print(PVL_likelihood)
print(EV_likelihood)
print(VSE_likelihood)
"""
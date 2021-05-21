import numpy as np
import random
import igt_game
import math

#r= [0] * 4
##w = 1 #loss aversion parameter
#u =[0]*4
#a = 0.2 #recency parameter
#Ev = [1] *4
#prob =[0.25]*4
#c = 2.7
#shape = 0.8
options = []
rewards = []

"""
agent that plays the igt using pvl model
"""

def prospectUtility(k,reward,u,w,shape):
    if reward >=0: u[k] = reward**shape
    else:
        u[k] = -w*abs(reward)**shape 
    return u

def learning(k, Ev , a, u):
    for e in range(4):
        Ev[e] = a*Ev[e]
        if e ==k: Ev[e]+=u[k]
    return Ev

def updateProb(prob , c, Ev): 
    
    theta = (math.pow(3,c)-1)
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    rounded = [round(e,4) for e in prob]
    prob0 = [x if x> 0 else 0.0001 for x in prob]
    return prob0
    

def chooseBox(prob):
    p = sum(prob)
    prob0 = [x/p for x in prob] #normalise valeus to avoid bug "values do not sum to 1"
    box = np.random.choice([0,1,2,3], p=prob0)
    return box


def playRoundPVL(w, u, a, Ev, prob, c,shape):
    global options
    global rewards
   # print(f"\n")
    k = chooseBox(prob)
    options.append(k)
   # print("choosing: ", k)

    reward = igt_game.drawPrize(k)
    rewards.append(reward)
   # print("Reward: ", reward)

    u_updated = prospectUtility(k,reward,u,w,shape)
    Ev_updated = learning(k, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated)
    #print("Actual Values: ",r)
    return reward, u_updated, Ev_updated, prob_updated

def startGame(w, u, a, Ev, prob, c, length,shape):
    rewardTotal = 0
    reward, u_updated, Ev_updated, prob_updated= playRoundPVL(w, u, a, Ev, prob, c,shape)
    for i in range(length):
        reward, u_updated, Ev_updated, prob_updated = playRoundPVL(w, u_updated, a, Ev_updated, prob_updated, c,shape)
        rewardTotal += reward
    return rewards, options
        
       
#r = game.generateRewardRates()
#startGame(w, u, a, Ev, prob, c, 10000,shape)

def participantCalc(w, u , a, Ev, prob, c, shape, reward, option,penalty):
    u_updated = prospectUtility(option, reward-penalty, u,w,shape)
    Ev_updated = learning(option, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated)
    return u_updated, Ev_updated, prob_updated

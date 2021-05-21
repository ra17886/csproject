import numpy as np
import random
import game

#r= [0] * 4
#w = 1 #loss aversion parameter
#u =[0]*4
#a = 0.2 #recency parameter
#Ev = [1] *4
#prob =[0.25]*4
#c = 2.7
options = []
rewards = []

"""
PVL agent, plays a synthetic game in the startGame function
fitted to participant data with the participantCalc function
"""

def prospectUtility(k,reward,u,w):
    if reward ==1: u[k] = 1
    else: u[k] = -w #slightly adjusted from original to suit no reward vs reward
   # print("Utility: ", u)
    return u

def learning(k, Ev , a, u):
    for e in range(4):
        Ev[e] = round(a*Ev[e],6)
        if e ==k: Ev[e]+=u[k]
   # print("Learning: ", Ev)
    return Ev

def updateProb(prob , c, Ev): 
    
    theta = ((3**c)-1)
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    #rounded = [round(e,4) for e in prob]
   # print("Probabilities: ", rounded)
    prob0 = [x if x> 0 else 0.0001 for x in prob]
    return prob0
    

def chooseBox(prob):
    box = np.random.choice([0,1,2,3], p=prob)
    return box


def playRoundPVL(w, u, a, Ev, prob, c,rates):
    global options
    global rewards
    #print(f"\n")
    k = chooseBox(prob)
    options.append(k)
    #print("choosing: ", k)

    reward = game.drawPrize(rates,k)
    rewards.append(reward)
    #if reward ==1: print("Prize!")
   # else: print("no Prize")

    u_updated = prospectUtility(k,reward,u,w)
    Ev_updated = learning(k, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated)
    #print("Actual Values: ",r)
    return reward, u_updated, Ev_updated, prob_updated

def startGame(w, u, a, Ev, prob, c, length,rates):
    rewardTotal = 0
    reward, u_updated, Ev_updated, prob_updated= playRoundPVL(w, u, a, Ev, prob, c,rates)
    for i in range(length):
        reward, u_updated, Ev_updated, prob_updated = playRoundPVL(w, u_updated, a, Ev_updated, prob_updated, c,rates)
        rewardTotal += reward
    return rewards, options
        
       
#r = game.generateRewardRates()
#startGame(w, u, a, Ev, prob, c, 1000,r)

def participantCalc(w, u , a, Ev, prob, c, reward, option):
    u_updated = prospectUtility(option, reward, u,w)
    Ev_updated = learning(option, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated)
    return u_updated, Ev_updated, prob_updated
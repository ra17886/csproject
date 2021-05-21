import numpy as np
import random
import igt_game

"""
evpu agent for the igt task
"""
options = []
rewards = []

#w = 4 #loss aversion parameter
#u =[0]*4
#a = 0.9 #recency parameter
#Ev = [1] *4
#prob =[0.25]*4
#c = 2
#shape = 0.1
options = []
rewards = []


def prospectUtility(k,reward,u,w,shape):
    if reward >=0: u[k] = reward**shape
    else:
        u[k] = -w*abs(reward)**shape #slightly adjusted from original to suit no reward vs reward
  #  print("Utility: ", u)
    return u

def learningEVPU(k, Ev , a, u):
    for e in range(4):
        Ev[e] = (1-a)*Ev[e]+a*u[e]
  #  print("Learning: ", Ev)
    return Ev


def updateProb(prob , c, Ev,t):   
    theta =  ((t+1)/10)**c
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    rounded = [round(e,4) for e in prob]
   # print("Probabilities: ", rounded)
    prob0 = [x if x> 0 else 0.0001 for x in prob]
    return prob0


def chooseBox(prob):
    p = sum(prob)
    prob0 = [x/p for x in prob] #normalise valeus to avoid bug "values do not sum to 1"
    box = np.random.choice([0,1,2,3], p=prob0)
    return box

def playRoundEVPU(w, u, a, Ev, prob, c,shape,t):
    global options
    global rewards
    print(f"\n")
    k = chooseBox(prob)
    options.append(k)
    print("choosing: ", k)

    reward = igt_game.drawPrize(k)
    rewards.append(reward)
   # if reward ==1: print("Prize!")
   ## else: print("no Prize")

    u_updated = prospectUtility(k,reward,u,w,shape)
    Ev_updated = learningEVPU(k, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated,t)
   # print("Actual Values: ",r)
    return reward, u_updated, Ev_updated, prob_updated

def startGame(w, u, a, Ev, prob, c, length,shape):
    rewardTotal = 0
    reward, u_updated, Ev_updated, prob_updated= playRoundEVPU(w, u, a, Ev, prob, c,shape,0)
    for t in range(length):
        reward, u_updated, Ev_updated, prob_updated = playRoundEVPU(w, u_updated, a, Ev_updated, prob_updated, c,shape,t)
        rewardTotal += reward
       # print(rewardTotal)
    return rewards, options
        

def participantCalc(w,u,a,Ev,prob,c,shape,reward,option,penalty, t):
    u_updated = prospectUtility(option, reward-penalty, u,w,shape)
    Ev_updated = learningEVPU(option, Ev, a, u_updated)
    prob_updated = updateProb(prob, c, Ev_updated,t)
   # print(f"\n")
    return u_updated, Ev_updated, prob_updated,t
    
       
#r = game.generateRewardRates()
#startGame(w, u, a, Ev, prob, c, 1000,shape)
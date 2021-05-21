import numpy as np
import random
import game

#theta = 0 #{0,1}, value sensitivity parameter, not being used here
delta = 0.2 #{0,1}, decay parameter
alpha = 0.76 #{0,1}, learning rate
phi = 0 #unbounded, exploration bonus
c = 5 #{0,5}, randomness

options = []
rewards = []

"""
agent that plays a game using the vse model using the startGame function
participantCalc plays a round of the participants game
"""


def prospectUtility(k,reward,v):
    if reward ==1: v[k] = 1
    else: v[k] = 0 #slightly adjusted from original to suit no reward vs reward
    return v


def computeExploit(exploit,k,delta,v):
    for e in range(4):
        exploit[e] = round(delta*exploit[e],6)
        if e==k: exploit[e]+=v[k]
    return exploit

def computeExplore(explore,k,alpha,phi):
    for e in range(4):
        if e==k: explore[e] = 0
        else: explore[e] = explore[e] +alpha*(phi-explore[e])
    return explore

def updateProb(prob, c,exploit,explore): 
    
    theta = ((3**c)-1)
    Ev = np.add(exploit,explore)
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    rounded = [round(e,4) for e in prob]
   # print("Probabilities: ", rounded)
    prob0 = [x if x> 0 else 0.0001 for x in prob]
    return prob0
    

def chooseBox(prob):
    box = np.random.choice([0,1,2,3], p=prob)
    return box


def playRound(delta,alpha,phi,c,v,exploit,explore,prob,r):
    global options
    global rewards
   # print(f"\n")
    k = chooseBox(prob)
    options.append(k)
    #print("choosing: ", k)

    reward = game.drawPrize(r,k)
    rewards.append(reward)
   #if reward ==1: print("Prize!")
   # else: print("no Prize")

    v_1= prospectUtility(k,reward,v)
    exploit_1 = computeExploit(exploit,k,delta, v_1)
    explore_1 = computeExplore(explore,k,alpha,phi)
    prob_1 = updateProb(prob, c,exploit_1,explore_1)
    #print("Actual Values: ",r)
    return reward, v_1,exploit_1,explore_1,prob_1

def startGame(delta,alpha,phi,c,v,exploit,explore,prob,length,r):
    rewardTotal = 0
    reward, v_1, exploit_1,explore_1, prob_1 = playRound(delta,alpha,phi,c,v,exploit,explore,prob,r)
    for i in range(length):
        reward, v_1, exploit_1,explore_1, prob_1 = playRound(delta,alpha,phi,c,v,exploit,explore,prob,r)
        rewardTotal += reward
       # print(rewardTotal)
    return rewards, options
        
       
#r = game.generateRewardRates()
#exploit = [1]*4
#explore = [1]*4
#v = [0]*4
#prob = [0.25]*4
#startGame(delta, alpha, phi,c,v,exploit, explore, prob, 10000, r)

def participantCalc(delta,alpha,phi, v,explore,exploit, prob, c, reward, option):
    v_1= prospectUtility(option,reward,v)
    exploit_1 = computeExploit(exploit,option,delta, v_1)
    explore_1 = computeExplore(explore,option,alpha,phi)
    prob_1 = updateProb(prob, c,exploit_1,explore_1)
    return v_1,exploit_1,explore_1,prob_1
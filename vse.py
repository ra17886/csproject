import numpy as np
import random
import igt_game

theta = 0.8 #{0,1}, value sensitivity parameter
delta = 0.9 #{0,1}, decay parameter
alpha = 0.99 #{0,1}, learning rate
phi = 5 #unbounded, exploration bonus
c = 2 #{0,5}, randomness


options = []
rewards = []


def prospectUtility(k,reward,loss,v, theta):
    v[k] = reward**theta - abs(loss)**theta
    print("Utility: ", v)
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
    
    theta1 = ((3**c)-1)
    Ev = np.add(exploit,explore)
    b = max(Ev)*theta1
    t = sum([np.exp(theta1*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta1-b)/t
    rounded = [round(e,4) for e in prob]
    print("Probabilities: ", rounded)
    prob0 = [x if x> 0 else 0.0001 for x in prob]
    return prob0
    

def chooseBox(prob):
    p = sum(prob)
    prob0 = [x/p for x in prob] #normalise valeus to avoid bug "values do not sum to 1"
    box = np.random.choice([0,1,2,3], p=prob0)
    return box


def playRound(delta,alpha,phi,c,v,exploit,explore,prob,theta):
    global options
    global rewards
    print(f"\n")
    k = chooseBox(prob)
    options.append(k)
    print("choosing: ", k)

    reward,loss = igt_game.vse_drawPrize(k)
    rewards.append(reward)
   #if reward ==1: print("Prize!")
   # else: print("no Prize")

    v_1= prospectUtility(k,reward,loss,v,theta)
    exploit_1 = computeExploit(exploit,k,delta, v_1)
    explore_1 = computeExplore(explore,k,alpha,phi)
    prob_1 = updateProb(prob, c,exploit_1,explore_1)
    #print("Actual Values: ",r)
    return reward,loss, v_1,exploit_1,explore_1,prob_1

def startGame(delta,alpha,phi,c,v,exploit,explore,prob,length,theta):
    rewardTotal = 0
    reward,loss, v_1, exploit_1,explore_1, prob_1 = playRound(delta,alpha,phi,c,v,exploit,explore,prob,theta)
    for i in range(length):
        reward,loss, v_1, exploit_1,explore_1, prob_1 = playRound(delta,alpha,phi,c,v,exploit,explore,prob,theta)
        rewardTotal += reward
        rewardTotal -= loss
       # print(rewardTotal)
    return rewards, options
        
       
#r = game.generateRewardRates()
exploit = [1]*4
explore = [1]*4
v = [0]*4
prob = [0.25]*4
startGame(delta, alpha, phi,c,v,exploit, explore, prob, 20, theta)

def participantCalc(delta,alpha,phi, v,explore,exploit, prob, c, reward, option):
    v_1= prospectUtility(option,reward,v)
    exploit_1 = computeExploit(exploit,option,delta, v_1)
    explore_1 = computeExplore(explore,option,alpha,phi)
    prob_1 = updateProb(prob, c,exploit_1,explore_1)
    return v_1,exploit_1,explore_1,prob_1
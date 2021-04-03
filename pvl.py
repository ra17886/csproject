import numpy as np
import random
import game

r= [0] * 4
w = 1 #loss aversion parameter
u =[0]*4
a = 0.2 #recency parameter
Ev = [0.25] *4
prob =[0.25]*4
c = 2.7


def prospectUtility(k,reward,u):
    if reward ==1: u[k] = 1
    else: u[k] = -w #slightly adjusted from original to suit no reward vs reward
    print("Utility: ", u)
    return u

def learning(k, Ev , a):
    for e in range(4):
        Ev[e] = round(a*Ev[e],6)
        if e ==k: Ev[e]+=u[k]
    print("Learning: ", Ev)
    return Ev

def updateProb(prob , c): 
    
    theta = ((3**c)-1)
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    rounded = [round(e,4) for e in prob]
    print("Probabilities: ", rounded)
    return prob
    

def chooseBox(prob):
    box = np.random.choice([0,1,2,3], p=prob)
    return box

def playRoundPVL(w, u, a, Ev, prob, c):
    #rewrite this!!!!
    print(f"\n")
    k = chooseBox(prob)
    print("choosing: ", k)

    reward = game.drawPrize(r,k)
    if reward ==1: print("Prize!")
    else: print("no Prize")

    u_updated = prospectUtility(k,reward,u)
    Ev_updated = learning(k, Ev, a)
    prob_updated = updateProb(prob, c)
    print("Actual Values: ",r)
    return reward, u_updated, Ev_updated, prob_updated

def startGame(w, u, a, Ev, prob, c):
    rewardTotal = 0
    reward, u_updated, Ev_updated, prob_updated= playRoundPVL(w, u, a, Ev, prob, c)
    for i in range(1000):
        reward, u_updated, Ev_updated, prob_updated = playRoundPVL(w, u_updated, a, Ev_updated, prob_updated, c)
        rewardTotal += reward
        
       
#r = game.generateRewardRates()
#startGame(w, u, a, Ev, prob, c)
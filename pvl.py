import numpy as np
import random
import game

r= [0] * 4
w = 4 #loss aversion parameter
u =[0]*4
a = 0.2 #recency parameter
Ev = [0.25] *4
prob =[0.25]*4
c = 2.7


def prospectUtility(k,reward):
    global u
    if reward ==1: u[k] = 1
    else: u[k] = -w #slightly adjusted from original to suit no reward vs reward
    print("Prospect Utility: ", u)

def learning(k):
    global Ev
    global a
    for e in range(4):
        Ev[e] = round(a*Ev[e],6)
        if e ==k: Ev[e]+=u[k]
    print("Learning: ", Ev)

def updateProb(): 
    global prob
    global c
    
    theta = ((3**c)-1)
    b = max(Ev)*theta
    t = sum([np.exp(theta*e-b)for e in Ev])
    for p in range(4):
        prob[p] = np.exp(Ev[p]*theta-b)/t
    rounded = [round(e,4) for e in prob]
    print("Probabilities: ", rounded)
    

def chooseBox():
    global prob
    box = np.random.choice([0,1,2,3], p=prob)
    return box


def startGame():
    rewardTotal = 0
    for i in range(1000):
        print(f"\n")
        k = chooseBox()
        print("choosing: ", k)

        reward = game.drawPrize(r,k)
        rewardTotal+= reward
        if reward ==1: print("Prize!")
        else: print("no Prize")

        prospectUtility(k,reward)
        learning(k)
        updateProb()
        print("Actual Values: ",r)
        print("Total Reward: ", rewardTotal)
       

r = game.generateRewardRates()
startGame()
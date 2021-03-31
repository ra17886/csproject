import numpy as np
import random

r= [0] * 4
w = 1 #loss aversion parameter
u =[0]*4
a = 0.9 #recency parameter
Ev = [0.25] *4
prob =[0.25]*4
c = 4

def check(a,b):
    return a-b>0.1

def checkAll(a,b,c,d):
    return check(a,b) and check(a,c) and check(a,d) and check(b,c) and check(b,d) and check(c,d)

def generateRewardRates():
    global r
    while not checkAll(r[0],r[1],r[2],r[3]):
        r = [np.random.beta(2,2) for x in r]
    random.shuffle(r)

def resetParams():
    r= [0] * 4
    w = 1 #loss aversion parameter
    u =[0]*4
    a = 0.5 #recency parameter
    Ev = [0] *4
    prob =[0.25]*4
    c = 2.5

def drawPrize(box):
    n = np.random.rand()
    if r[box] > n: return 1
    else: return 0


def theta():
    global c
    return (3^c)-1

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

def total():
    global Ev
    global c
    b = Ev.max() #shift invariant
    theta = round((3**c)-1,6)
    l = [np.exp(theta*e-b) for e in Ev]
    return sum(l), b

def updateProb(): 
    global prob
    global c
    
    b = max(Ev)
    theta = ((3**c)-1)

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

        reward = drawPrize(k)
        rewardTotal+= reward
        if reward ==1: print("Prize!")
        else: print("no Prize")

        prospectUtility(k,reward)
        learning(k)
        updateProb()
        print("Actual Values: ",r)
        print("Total Reward: ", rewardTotal)




        

generateRewardRates()
startGame()
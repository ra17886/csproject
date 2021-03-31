import numpy as np
import random

r= [0] * 4
w = 3 #loss aversion parameter
u =[0.5]*4
a = 0.5 #recency parameter
Ev = [0.5] *4
prob =[0.5]*4
c = 2

def check(a,b):
    return a-b>0.1

def checkAll(a,b,c,d):
    return check(a,b) and check(a,c) and check(a,d) and check(b,c) and check(b,d) and check(c,d)

def generateRewardRates():
    global r
    while not checkAll(r[0],r[1],r[2],r[3]):
        r = [np.random.beta(2,2) for x in r]
    random.shuffle(r)
    print(r)

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
        Ev[e] = a*Ev[e]
        if e ==k: Ev[e]+=u[k]
    print("Learning: ", Ev)

def total():
    global Ev
    global c
    theta = (3^c)-1
    l = [np.exp(theta)*e for e in Ev]
    return sum(l)

def updateProb():
    global prob
    t = total()
    for p in range(4):
        prob[p] = Ev[p]/t
    print("Probabilities: ", prob)

def chooseBox():
    global prob
    return prob.index(max(prob))

def startGame():
    generateRewardRates()
    for i in range(12):
        k = chooseBox()
        print("choosing: ", k)

        reward = drawPrize(k)
        if reward ==1: print("Prize!")
        else: print("no Prize")

        prospectUtility(k,reward)
        learning(k)
        updateProb()


startGame()
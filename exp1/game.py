
import numpy as np 
import random 

"""
A script to play a multi-armed bandit game, generates reward rates from a Beta(2,2) distribution, ensuring they are all 0.1 apart
This script is imported into most of the models and used there
"""

def check(a,b):
    return a-b>0.1

def checkAll(a,b,c,d):
    return check(a,b) and check(a,c) and check(a,d) and check(b,c) and check(b,d) and check(c,d)

def generateRewardRates():
    r = [0]*4
    while not checkAll(r[0],r[1],r[2],r[3]):
        r = [np.random.beta(2,2) for x in r]
    random.shuffle(r)
    return r

def drawPrize(r,box):
    n = np.random.rand()
    if r[box] > n: return 1
    else: return 0

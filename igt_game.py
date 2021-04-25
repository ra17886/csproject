
import numpy as np 
import random 



def drawPrize(box):
    n = np.random.rand()
    reward = 0
    if box == 0:
        reward += 100
        if n<0.5: reward -=250
    elif box == 1:
        reward += 100
        if n<0.1: reward -=1250
    elif box ==2:
        reward += 50
        if n<0.5: reward -=50
    elif box ==3:
        reward +=50
        if n<0.1: reward -=250
    
    return reward

def vse_drawPrize(box):
    n = np.random.rand()
    reward = 0
    loss = 0
    if box == 0:
        reward += 100
        if n<0.5: loss -=250
    elif box == 1:
        reward += 100
        if n<0.1: loss -=1250
    elif box ==2:
        reward += 50
        if n<0.5: loss -=50
    elif box ==3:
        reward +=50
        if n<0.1: loss -=250
    
    return reward, loss
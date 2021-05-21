import numpy as np
import random
import igt_game

#theta = 0.8 #{0,1}, value sensitivity parameter
#elta = 0.9 #{0,1}, decay parameter
#alpha = 0.99 #{0,1}, learning rate
#phi = 5 #unbounded, exploration bonus
#c = 2 #{0,5}, randomness

"""
plays a win stay lose shift model for igt game, not yet finished/checked
i am sure there are bugs here but nnot sure where
"""

options = []
rewards = []
    
def chooseBox(prob):
    p = sum(prob)
    prob0 = [x/p for x in prob] #normalise valeus to avoid bug "values do not sum to 1"
    box = np.random.choice([0,1,2,3], p=prob0)
    return box

def chooseStay(p,box):
    n = np.random.rand()

    stay = False
    if n<p: stay=True

    if stay: 
        print("staying")
        return box
        
    else: 
        k=box
        print("shifting")
        while(k ==box):
         k = np.random.choice([0,1,2,3])
        return k

def chooseShift(p,box):
    n = np.random.rand()

    shift = False
    if n<p: shift=True

    if not shift:
        print("staying") 
        return box
        
    else: 
        k=box
        print("shifting")
        while(k ==box):
         k = np.random.choice([0,1,2,3])
        return k

def playRound(p_stay,p_shift,box,reward):
    global options
    global rewards
    print(f"\n")
    if reward>=0: k=chooseStay(p_stay,box)
    else: k=chooseShift(p_shift,box)
    options.append(k)
    print("choosing: ", k)

    reward = igt_game.drawPrize(k)
    rewards.append(reward)
  #  if reward ==1: print("Prize!")
  #  else: print("no Prize")

    #print("Actual Values: ",r)
    return reward,k

def startGame(p_stay,p_shift,length):
    rewardTotal = 0
    box = np.random.choice([0,1,2,3])
    reward = 0
    reward, box = playRound(p_stay,p_shift,box,reward)
    for i in range(length):
        reward,box = playRound(p_stay,p_shift,box,reward)
        rewardTotal += reward
        print(rewardTotal)
    return rewards, options
        

#p_stay = 0.9
#p_shift = 0.8
#startGame(p_stay,p_shift,100)


def participantCalc(p_stay,p_shift,option1,reward,option2):
    if reward>0:
        if option1==option2:return p_stay
        else: return 1-p_stay
    else:
        if option1==option2: return 1-p_shift
        else:return p_shift
    
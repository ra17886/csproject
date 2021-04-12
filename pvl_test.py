#take in jsons
#extract wac

#play game with wac values
#get reward and options chosen

#run log likelihood on the values to see what wac are extracted

import json 
import pvl 
import os
import optimise
import numpy 
w_values = [[]] #first is estimated, second is actual
a_values = [[]]
c_values = [[]]

def play(w,a,c,n,rates):
    u = [0]*4
    Ev = [0.25]*4
    prob = [0.25]*4
    return pvl.startGame(w,u,a,Ev,prob,c,n,rates)

def check(probs):
    done = True
    for p in probs:
        if p==1: 
            done = False
    return done

def extractRates(data):
    rates = data['rates']
    options = data['options']
    probs = [1,1,1,1]
    i = 0
    while not check(probs) and i!=len(rates)-1:
        if probs[options[i]] ==1:
            probs[options[i]] = rates[i]
        i+=1
    total = numpy.sum(probs)
    n = 0
    for i in probs: 
        if i ==1: n+=1
    probs = [(1-(total-n))/n if x==1 else x for x in probs]
    return(probs)

def start(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            rates = extractRates(data)
            rewards, options = play(data['w'], data['a'], data["c"], data["length"],rates)
            v = [data['w'], data['a'], data["c"]]
            
            likelihood , w, a, c = optimise.run_optimiser(rewards,options,rates)
            w_values.append([w,data['w']])
            a_values.append([a,data['a']])
            c_values.append([c,data['c']])
            print('filename')
    f = open("w_estimation.txt","w")
    for row in w_values:
        numpy.savetxt(f,row)
    f.close()
    f1 = open("a_estimation.txt","w")
    for row in a_values:
        numpy.savetxt(f1,row)
    f1.close()
    f2 = open("c_estimation.txt","w")
    for row in c_values:
        numpy.savetxt(f2,row)
    f2.close()
    

directory = "pvl_trial/"
start(directory)
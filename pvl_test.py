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
import matplotlib.pyplot as plt 
w_values = [] #first is estimated, second is actual
a_values = []
c_values = []
e_w_values = [] 
e_a_values = []
e_c_values = []

#plays a game with the given parameters
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

def computeAccuracy(w,a,c):
    w_accuracy = [x[0]-x[1] for x in w]
    a_accuracy = [x[0]-x[1] for x in a]
    c_accuracy = [x[0]-x[1] for x in c]
    accuracy = [w_accuracy, a_accuracy, c_accuracy]
    fig, ax = plt.subplots()
    ax.set_title('Accuracy of estimated parameters')
    ax.boxplot(accuracy)

    plt.show()

def start(directory):
    n = 0
    for filename in os.listdir(directory):
        if numpy.random.rand() > 0: #how many of the results do we want to check?
            if filename.endswith(".json"):
                print(n)
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                rates = extractRates(data)
            
                #PVL test
                rewards, options = play(data['w'], data['a'], data["c"], 1000,rates) #plays a game 
                v = [data['w'], data['a'], data["c"]]
                likelihood , w, a, c = optimise.run_optimiser(rewards,options,'p')
                w_values.append([w,data['w']])
                a_values.append([a,data['a']])
                c_values.append([c,data['c']])


                #EVPU test
                e_rewards, e_options = play(data['EVPU_w'], data['EVPU_a'], data["EVPU_c"], 1000,rates) #plays a game 
                e_v = [data['EVPU_w'], data['EVPU_a'], data["EVPU_c"]]
                likelihood , e_w, e_a, e_c = optimise.run_optimiser(e_rewards,e_options,'e')
                e_w_values.append([e_w,data['EVPU_w']])
                e_a_values.append([a,data['EVPU_a']])
                e_c_values.append([c,data['EVPU_c']])
                n+=1

    computeAccuracy(w_values,a_values,c_values)
    computeAccuracy(e_w_values,e_a_values,e_c_values)
   
   

    


directory = "evpu_trial/"
start(directory)
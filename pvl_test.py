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
        if numpy.random.rand() > 0:
            print("testing")
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
                print(filename)
    print(w_values)
    print(a_values)
    print(c_values)
    w_accuracy = [x[0]-x[1] for x in w_values]
    a_accuracy = [x[0]-x[1] for x in a_values]
    c_accuracy = [x[0]-x[1] for x in c_values]
    print(w_accuracy)
    print(a_accuracy)
    print(c_accuracy)

    accuracy = [w_accuracy, a_accuracy, c_accuracy]
    fig, ax = plt.subplots()
    ax.set_title('Accuracy of estimated parameters')
    ax.boxplot(accuracy)

    plt.show()



directory = "pvl_trial/"
start(directory)
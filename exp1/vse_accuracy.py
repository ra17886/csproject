import json 
import vse
import os
import vse_optimise
import numpy 
import matplotlib.pyplot as plt 
alpha_values = [] #first is estimated, second is actual
delta_values = []
phi_values = []
c_values = []

"""
Parameter recovery for the VSE model
"""

def play(alpha,delta,phi,c,n,rates):
    v= [1]*4
    explore = [1]*4
    exploit = [1]*4
    prob = [0.25]*4
    return vse.startGame(alpha,delta,phi,c,v,explore,exploit,prob,n,rates)

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

def computeAccuracy(a,d,p,c):
    alpha_accuracy = [x[0]-x[1] for x in a]
    delta_accuracy = [x[0]-x[1] for x in d]
    phi_accuracy = [x[0]-x[1] for x in p]
    c_accuracy = [x[0]-x[1] for x in c]
    accuracy = [alpha_accuracy, delta_accuracy, phi_accuracy,c_accuracy]
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
                print(n, "Extracting rates")
                rates = extractRates(data)
            
                #VSE test
                alpha = data["VSE_alpha"]
                delta = data["VSE_delta"]
                phi = data["VSE_phi"]
                c = data["VSE_c"]
                print(n," Playing")
                rewards, options = play(alpha,delta,phi,c,1000,rates) #plays a game 
                print(n, "Optimising")
                likelihood_e,delta_e,alpha_e,phi_e,c_e = vse_optimise.run_optimiser(rewards,options)
                alpha_values.append([alpha,alpha_e])
                delta_values.append([delta,delta_e])
                phi_values.append([phi,phi_e])
                c_values.append([c,c_e])
        n+=1

    computeAccuracy(alpha_values,delta_values,phi_values,c_values)

#directory = 'vse_trial/'
#start(directory)

import json 
import pvl 
import os
import os.path
import optimise
import numpy 
import matplotlib.pyplot as plt 
import vse_accuracy
import vse_optimise

"""
This module takes a model and participant, plays a game using the estimated parameters for the participant and
then runs the optimise module this synthetic game data
There are lots of errors here, particularly with the distiction between the EV-PU game and PVL game, they need separate functions 
but this has not been implemented correctly
"""


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

def createDict(actual,estimate):
    d = dict()
    d['actual'] = actual
    d['estimate'] = estimate
    return d

def PVL(rates, data):
    rewards, options = play(data['w'], data['a'], data["c"], 1000,rates) #plays a game 
    likelihood , w, a, c = optimise.run_optimiser(rewards,options,'p')
    w_values=createDict(data['w'],w)
    a_values=createDict(data['a'],a)
    c_values=createDict(data['c'],c)

    return [w_values, a_values, c_values]

def EVPU(rates,data):
    e_rewards, e_options = play(data['EVPU_w'], data['EVPU_a'], data["EVPU_c"], 1000,rates) #plays a game #needs to be changed to EV-PU play
    likelihood , w, a, c = optimise.run_optimiser(e_rewards,e_options,'e')
    w_values=createDict(data['EVPU_w'],w)
    a_values=createDict(data['EVPU_a'],a)
    c_values=createDict(data['EVPU_c'],c)
    return [w_values, a_values, c_values]

def VSE(rates,data):
    alpha = data["VSE_alpha"]
    delta = data["VSE_delta"]
    phi = data["VSE_phi"]
    c = data["VSE_c"]
    rewards, options = vse_accuracy.play(alpha,delta,phi,c,1000,rates) #plays a game 
    likelihood_e,delta_e,alpha_e,phi_e,c_e = vse_optimise.run_optimiser(rewards,options)
    alpha_values = createDict(alpha,alpha_e)
    delta_values= createDict(delta,delta_e)
    phi_values= createDict(phi,phi_e)
    c_values= createDict(c,c_e)
    return [alpha_values,delta_values,phi_values,c_values]


def saveFile(data, filename):
    n = 'model_accuracy/' + filename
    with open(n, "x") as f:
        json.dump(data,f)
        print('saved ', n)

def start(directory):
    n = 0
    for filename in os.listdir(directory):
        if numpy.random.rand() > 0: #how many of the results do we want to check?
            file_path = os.path.join('model_accuracy',filename)
            if filename.endswith(".json") and not (os.path.isfile(file_path)):
                print(n)
                d = dict()
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                rates = extractRates(data)
            
                #PVL test
                vPVL = PVL(rates,data)
                d["PVL_w"] = vPVL[0]
                d["PVL_a"] = vPVL[1]
                d["PVL_c"] = vPVL[2]

                #EVPU test
                vEVPU = EVPU(rates,data)
                d["EVPU_w"] = vEVPU[0]
                d["EVPU_a"] = vEVPU[1]
                d["EVPU_c"] = vEVPU[2]

                #VSE test
                vVSE = VSE(rates,data)
                d["VSE_alpha"] = vVSE[0]
                d["VSE_delta"] = vVSE[1]
                d["VSE_phi"] = vVSE[2]
                d["VSE_c"] = vVSE[3]
                
                saveFile(d,filename)
            n+=1


    #computeAccuracy(w_values,a_values,c_values)
    #computeAccuracy(e_w_values,e_a_values,e_c_values)
   
   

    


directory = "vse_trial/"
start(directory)
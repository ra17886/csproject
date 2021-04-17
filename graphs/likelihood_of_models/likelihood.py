import os
import json
import matplotlib.pyplot as plt 
import numpy as np 

#work out relationship between likelihoods and affective state
#get overall happiness score and plot scatter graph between likelihoods

directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/evpu2_trial/'

def computeScore(d):
    return d['NA_score']+d['PHQ_score']+d['GAD_score']-d['PA_score']

def getData(directory):
    scores = []
    PVL = []
    PVL2 = []
    EVPU = []
    EVPU2 = []
    for filename in os.listdir(directory):
            if filename.endswith(".json"):
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                scores.append(computeScore(data))
                PVL.append(data['likelihood'])
                PVL2.append(data['PVL2_likelihood'])
                EVPU.append(data['EVPU_likelihood'])
                EVPU2.append(data['EVPU2_likelihood'])
    return [scores, PVL, PVL2, EVPU, EVPU2]

def plot(x,y,y_label):
    plt.figure(figsize=[10,8])
    plt.scatter(x, y)

    nx = np.array(x)
    ny = np.array(y)
    m, b = np.polyfit(nx, ny, 1)

    plt.plot(nx, m*nx + b)
    plt.xlabel('Negativity Scores')
    plt.ylabel(y_label + ' Likelihood')
    plt.title('Negativity Score and ' + y_label +  ' Model Correlation')
    plt.show()


data = getData(directory)
plot(data[0],data[1],'PVL')
plot(data[0],data[2],'PVL2')
plot(data[0],data[3],'EVPU')
plot(data[0],data[4],'EVPU2')
   


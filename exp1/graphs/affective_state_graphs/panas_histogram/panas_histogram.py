import numpy as numpy
import matplotlib.pyplot as plt


import os
import json

def getPANASscores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/pvl_trial'
    panas = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            panas.append(data['NA_score']-data['PA_score'])
    return panas

def savePANASscores(panas):
    with open("panas_data.txt","w") as f:
        for line in panas:
            f.write(str(line) + ",")
    f.close()

def createHistogram(panas):
    plt.figure(figsize=[10,8])
    n, bins, patches = plt.hist(x=panas,bins=12)
    plt.xlabel('PANAS Scores')
    plt.ylabel('Frequency',fontsize=15)
    plt.title('PANAS (Negative Affect-Positive Affect) Score Frequency',fontsize=15)
    plt.show()

panas = getPANASscores()
savePANASscores(panas)
createHistogram(panas)
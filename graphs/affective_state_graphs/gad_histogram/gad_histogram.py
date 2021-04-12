import numpy as numpy
import matplotlib.pyplot as plt


import os
import json

def getGADscores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/pvl_trial'
    GAD = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            GAD.append(data['GAD_score'])
    return GAD

def saveGADscores(GAD):
    with open("gad_data.txt","w") as f:
        for line in GAD:
            f.write(str(line) + ",")
    f.close()

def createHistogram(GAD):
    plt.figure(figsize=[10,8])
    n, bins, patches = plt.hist(x=GAD,bins=12)
    plt.xlabel('GAD Scores')
    plt.ylabel('Frequency',fontsize=15)
    plt.title('GAD Score Frequency',fontsize=15)
    plt.show()

GAD = getGADscores()
saveGADscores(GAD)
createHistogram(GAD)
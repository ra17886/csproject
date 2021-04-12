import numpy as numpy
import matplotlib.pyplot as plt


import os
import json

def getPHQscores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/pvl_trial'
    PHQ = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            PHQ.append(data['PHQ_score'])
    return PHQ

def savePHQscores(PHQ):
    with open("phq_data.txt","w") as f:
        for line in PHQ:
            f.write(str(line) + ",")
    f.close()

def createHistogram(PHQ):
    plt.figure(figsize=[10,8])
    n, bins, patches = plt.hist(x=PHQ,bins=12)
    plt.xlabel('PHQ Scores')
    plt.ylabel('Frequency',fontsize=15)
    plt.title('PHQ Score Frequency',fontsize=15)
    plt.show()

PHQ = getPHQscores()
#savePHQscores(PHQ)
createHistogram(PHQ)
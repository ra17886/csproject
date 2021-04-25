import numpy as np 
import matplotlib.pyplot as plt 
import json 
import os


def getGAD_PHQscores():
    directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/pvl_trial'
    GAD = []
    PHQ = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file = open(os.path.join(directory, filename),'r')
            data = json.load(json_file)
            GAD.append(data['GAD_score'])
            PHQ.append(data['PHQ_score'])
    return GAD, PHQ

def saveGAD_PHQscores(GAD, PHQ):
    with open("data.txt","w") as f:
        f.write("GAD:")
        for line in GAD:
            f.write(str(line) + ",")
        f.write("PHQ:")
        for line in PHQ:
            f.write(str(line)+",")
    f.close()

def createScatterGraph(GAD,PHQ):
    plt.figure(figsize=[10,8])
    plt.scatter(GAD, PHQ)
    x = np.array(GAD)
    y = np.array(PHQ)
    m, b = np.polyfit(x, y, 1)

    plt.plot(x, m*x + b)
    plt.xlabel('GAD Scores')
    plt.ylabel('PHQ Scores')
    plt.title('GAD and PHQ Correlation')
    plt.show()

GAD, PHQ = getGAD_PHQscores()
saveGAD_PHQscores(GAD,PHQ)
createScatterGraph(GAD, PHQ)
import os
import json
import numpy as np 
import matplotlib.pyplot as plt
from math import exp
"""
computes the most likely model more each partcipants and plots on a scatter graph 
while applying a line of best fit
"""
def computeScore(d):
    return d['NA_score']+d['PHQ_score']+d['GAD_score']-d['PA_score']

def getData(directory):
    scores = []
    PVL = []
    PVL2 = []
    EVPU = []
    EVPU2 = []
    vse=[]
    GAD =[]
    PHQ = []
    wsls = []
    for filename in os.listdir(directory):
            if filename.endswith(".json"):
                json_file = open(os.path.join(directory, filename),'r')
                data = json.load(json_file)
                scores.append(computeScore(data))
                GAD.append(data['GAD_score'])
                PHQ.append(data['PHQ_score'])
                PVL.append(data['pvl_likelihood'])
                EVPU.append(data['evpu_likelihood'])
                vse.append(data['vse_likelihood'])
    return [scores,GAD,PHQ ,PVL, EVPU,vse]

def BIC(l,k):
    return k*np.log(46)+2*l

def computeMostLikely(pvl,evpu,vse):
    #print(pvl, " ",pvl2," ",evpu, " ",evpu2," ",vse," ",wsls)
    bics = {BIC(pvl,3): "PVL", BIC(evpu,3): "EVPU",BIC(vse,4):"VSE"}
    #print(bics)
    print(bics.get(min(bics)))
    return bics.get(min(bics))

def computeEach(data):
    plot_pvl = []
    plot_evpu = []
    plot_vse = []
    for i in range(len(data[0])):
        most_likely = computeMostLikely(data[3][i],data[4][i],data[5][i])
        if most_likely == "PVL" : plot_pvl.append([data[0][i],data[1][i],data[2][i],data[3][i]])
        if most_likely == "EVPU" : plot_evpu.append([data[0][i],data[1][i],data[2][i],data[4][i]])
        if most_likely == "VSE" : plot_vse.append([data[0][i],data[1][i],data[2][i],data[5][i]])
    return plot_pvl,plot_evpu,plot_vse

 #returns score,GAD,PHQ,likelihood

directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/final_trial'
data = getData(directory)
pvl,evpu,vse, = computeEach(data)

fig, ax = plt.subplots()

pvl_x = [pvl[i][0] for i in range(len(pvl))]
pvl_y = [-pvl[i][3] for i in range(len(pvl))]

ax.scatter(pvl_x, pvl_y, c='blue',  label="PVL")
x = np.array(pvl_x)
y = np.array(pvl_y)
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b,c ="blue")


evpu_x = [evpu[i][0] for i in range(len(evpu))]
evpu_y = [-evpu[i][3] for i in range(len(evpu))]
ax.scatter(evpu_x, evpu_y, c='green',  label="EVPU")
x = np.array(evpu_x)
y = np.array(evpu_y)
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b,c ="green")


vse_x = [vse[i][0] for i in range(len(vse))]
vse_y = [-vse[i][3] for i in range(len(vse))]
ax.scatter(vse_x, vse_y, c='red',  label="VSE")
x = np.array(vse_x)
y = np.array(vse_y)
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b,c ="red")



ax.legend()

plt.xlabel("Overall Negativity")
plt.ylabel("Model Log-Likelihood")

plt.show()
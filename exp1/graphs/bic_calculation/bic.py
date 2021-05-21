import os
import json
import numpy as np 
import matplotlib.pyplot as plt

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
                PVL.append(data['likelihood'])
                PVL2.append(data['PVL2_likelihood'])
                EVPU.append(data['EVPU_likelihood'])
                EVPU2.append(data['EVPU2_likelihood'])
                vse.append(data['VSE_likelihood'])
                wsls.append(data["WSLS_likelihood"])
    return [scores,GAD,PHQ ,PVL, PVL2, EVPU, EVPU2,vse,wsls]

def BIC(l,k):
    return k*np.log(46)+2*l

def computeMostLikely(pvl,pvl2,evpu,evpu2,vse,wsls):
    #print(pvl, " ",pvl2," ",evpu, " ",evpu2," ",vse," ",wsls)
    bics = {BIC(pvl,3): "PVL", BIC(pvl2,2): "PVL2", BIC(evpu,3): "EVPU",BIC(evpu2,2):"EVPU2",BIC(vse,4):"VSE",BIC(wsls,2):"WSLS"}
    #print(bics)
    print(bics.get(min(bics)))
    return bics.get(min(bics))

def computeEach(data):
    plot_pvl = []
    plot_pvl2 = []
    plot_evpu = []
    plot_evpu2 = []
    plot_vse = []
    plot_wsls = []
    for i in range(len(data[0])):
        most_likely = computeMostLikely(data[3][i],data[4][i],data[5][i],data[6][i],data[7][i],data[8][i])
        if most_likely == "PVL" : plot_pvl.append([data[0][i],data[1][i],data[2][i],data[3][i]])
        if most_likely == "PVL2" : plot_pvl2.append([data[0][i],data[1][i],data[2][i],data[4][i]])
        if most_likely == "EVPU" : plot_evpu.append([data[0][i],data[1][i],data[2][i],data[5][i]])
        if most_likely == "EVPU2" : plot_evpu2.append([data[0][i],data[1][i],data[2][i],data[6][i]])
        if most_likely == "VSE" : plot_vse.append([data[0][i],data[1][i],data[2][i],data[7][i]])
        if most_likely == "WSLS" : plot_wsls.append([data[0][i],data[1][i],data[2][i],data[8][i]])
    return plot_pvl,plot_pvl2,plot_evpu,plot_evpu2,plot_vse,plot_wsls

 

directory = '/Users/roshanark/Documents/UNI/4th Year/Dissertation/roshan/exp1/wsls_trial/'
data = getData(directory)
pvl,pvl2,evpu,evpu2,vse,wsls = computeEach(data)

fig, ax = plt.subplots()
ax.scatter([pvl[i][2]for i in range(len(pvl))], [pvl[i][3]for i in range(len(pvl))], c='blue',  label="PVL")
ax.scatter([pvl2[i][2]for i in range(len(pvl2))], [pvl2[i][3]for i in range(len(pvl2))], c='orange',  label="PVL2")
ax.scatter([evpu[i][2]for i in range(len(evpu))], [evpu[i][3]for i in range(len(evpu))], c='green',  label="EVPU")
ax.scatter([evpu2[i][2]for i in range(len(evpu2))], [evpu2[i][3]for i in range(len(evpu2))], c='purple',  label="EVPU2")
ax.scatter([vse[i][2]for i in range(len(vse))], [vse[i][3]for i in range(len(vse))], c='red',  label="VSE")
ax.scatter([wsls[i][2]for i in range(len(wsls))], [wsls[i][3]for i in range(len(wsls))], c='pink',  label="WSLS")
ax.legend()

plt.xlabel("PHQ-9 Score")
plt.ylabel("Model Likelihood")

plt.show()